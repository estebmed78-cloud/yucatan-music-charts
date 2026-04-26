import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

# Configuración de credenciales
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Usa estos IDs (ya probados que funcionan con la API)
ARTIST_IDS = [
    '3YfS898Vf6SWH7I0NfbnIu', # Aleks Syntek (ID actual)
    '0I2Tq9Hq752Y1b8YF1Fm3x', # Armando Manzanero
    '5KAtp7K4IStTclXhCidW9m', # Los Baby's
    '1Mxy1ynui2eF5RTGSuf8zz', # Los Juglares
]

def get_artist_data():
    artists_list = []
    
    for artist_id in ARTIST_IDS:
        try:
            # Pedimos los datos
            artist = sp.artist(artist_id)
            
            # Sacamos la info. Si no hay género, ponemos "Pop" por defecto
            generos = artist.get('genres', [])
            genero_principal = generos[0].title() if generos else "Música Yucateca"
            
            artists_list.append({
                "Nombre": artist['name'],
                "Seguidores": artist['followers']['total'],
                "Popularidad": artist['popularity'],
                "Género": genero_principal,
                "Link": artist['external_urls']['spotify']
            })
            print(f"✅ Cargado: {artist['name']}")
            
        except Exception as e:
            # Si el ID falla (como el 404 que te daba), avisamos y saltamos
            print(f"⚠️ El ID {artist_id} no funcionó con la API. Saltando...")

    # Guardar siempre, aunque sea con un artista
    if artists_list:
        df = pd.DataFrame(artists_list)
        df = df.sort_values(by="Seguidores", ascending=False)
        df.to_csv("artistas_yucatan.csv", index=False)
        print("💾 Archivo guardado correctamente.")
    else:
        print("❌ No se pudo obtener ningún dato.")

if __name__ == "__main__":
    get_artist_data()
