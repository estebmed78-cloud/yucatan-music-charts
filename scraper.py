import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import os

# Lista de IDs de artistas (estos IDs sí funcionan para la web)
ARTIST_IDS = [
    '3YfS898Vf6SWH7I0NfbnIu', # Aleks Syntek
    '0I2Tq9Hq752Y1b8YF1Fm3x', # Armando Manzanero
    '5KAtp7K4IStTclXhCidW9m', # Los Baby's
]

def get_monthly_listeners(artist_id):
    url = f"https://open.spotify.com/intl-es/artist/{artist_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos el texto que dice "oyentes mensuales"
        meta_description = soup.find('meta', property='og:description')
        if meta_description:
            content = meta_description['content']
            # Extraemos el número del texto "X oyentes mensuales"
            number = re.search(r'([\d.,]+)', content)
            if number:
                # Limpiamos el número (quitamos comas y puntos)
                clean_number = int(number.group(1).replace('.', '').replace(',', ''))
                return clean_number
    except Exception as e:
        print(f"Error con ID {artist_id}: {e}")
    return 0

def update_chart():
    filename = 'artistas_yucatan.csv'
    
    # Intentamos cargar datos anteriores para calcular Daily +/- y Peak
    if os.path.exists(filename):
        df_old = pd.read_csv(filename)
    else:
        df_old = pd.DataFrame(columns=['ID', 'Nombre', 'Listeners', 'Daily', 'Peak'])

    new_data = []

    for artist_id in ARTIST_IDS:
        # 1. Obtener nombre (solo para el primer registro)
        # Aquí usamos un truco simple o mantenemos una lista
        nombre = "Artista " + artist_id # Simplificado para el ejemplo
        if artist_id == '3YfS898Vf6SWH7I0NfbnIu': nombre = "Aleks Syntek"
        if artist_id == '0I2Tq9Hq752Y1b8YF1Fm3x': nombre = "Armando Manzanero"
        if artist_id == '5KAtp7K4IStTclXhCidW9m': nombre = "Los Baby's"

        # 2. Obtener Oyentes Mensuales Actuales
        current_listeners = get_monthly_listeners(artist_id)
        
        # 3. Calcular Daily +/-
        daily_change = 0
        peak = current_listeners
        
        if not df_old.empty and artist_id in df_old['ID'].values:
            old_row = df_old[df_old['ID'] == artist_id].iloc[0]
            daily_change = current_listeners - old_row['Listeners']
            # Mantener el Peak histórico
            peak = max(current_listeners, old_row['Peak'])

        new_data.append({
            'ID': artist_id,
            'Nombre': nombre,
            'Listeners': current_listeners,
            'Daily': daily_change,
            'Peak': peak
        })

    df_new = pd.DataFrame(new_data)
    df_new = df_new.sort_values(by='Listeners', ascending=False)
    df_new.to_csv(filename, index=False)
    print("Datos actualizados estilo Kworb.")

if __name__ == "__main__":
    update_chart()
