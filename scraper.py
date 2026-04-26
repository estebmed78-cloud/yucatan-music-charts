import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

# LISTA DE IDs (Usa los que a ti te funcionan)
ARTIST_IDS = [
    '0r8toju2ecKaVtItkzAnNi', # Aleks Syntek (Tu ID)
    '0I2Tq9Hq752Y1b8YF1Fm3x', # Armando Manzanero
    '5KAtp7K4IStTclXhCidW9m', # Los Baby's
]

def get_spotify_data(artist_id):
    url = f"https://open.spotify.com/intl-es/artist/{artist_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Obtener Nombre del Artista
        nombre = soup.find('meta', property='og:title')['content'].replace(' | Spotify', '')
        
        # 2. Obtener Oyentes Mensuales desde el meta tag
        # Ejemplo: "Aleks Syntek · Artista · 4.8M oyentes mensuales."
        description = soup.find('meta', property='og:description')['content']
        
        # Buscamos el número que acompaña a "oyentes mensuales"
        match = re.search(r'([\d.,]+[MK]?) oyentes mensuales', description)
        if match:
            raw_val = match.group(1).replace(',', '')
            # Convertimos K (miles) y M (millones) a números reales
            if 'M' in raw_val:
                listeners = int(float(raw_val.replace('M', '')) * 1000000)
            elif 'K' in raw_val:
                listeners = int(float(raw_val.replace('K', '')) * 1000)
            else:
                listeners = int(raw_val)
            return nombre, listeners
    except Exception as e:
        print(f"Error con ID {artist_id}: {e}")
    return None, 0

def run_scraper():
    filename = 'artistas_yucatan.csv'
    
    # Cargar datos anteriores si existen para calcular Daily y Peak
    if os.path.exists(filename):
        df_old = pd.read_csv(filename)
    else:
        df_old = pd.DataFrame(columns=['ID', 'Nombre', 'Listeners', 'Daily', 'Peak'])

    results = []
    for artist_id in ARTIST_IDS:
        nombre, current_listeners = get_spotify_data(artist_id)
        if nombre:
            # Calcular cambios
            daily = 0
            peak = current_listeners
            
            if artist_id in df_old['ID'].values:
                prev_val = df_old.loc[df_old['ID'] == artist_id, 'Listeners'].values[0]
                prev_peak = df_old.loc[df_old['ID'] == artist_id, 'Peak'].values[0]
                daily = current_listeners - prev_val
                peak = max(current_listeners, prev_peak)
            
            results.append({
                'ID': artist_id,
                'Nombre': nombre,
                'Listeners': current_listeners,
                'Daily': daily,
                'Peak': peak
            })
            print(f"✅ {nombre}: {current_listeners} oyentes")

    df_final = pd.DataFrame(results).sort_values(by='Listeners', ascending=False)
    df_final.to_csv(filename, index=False)

if __name__ == "__main__":
    run_scraper()
