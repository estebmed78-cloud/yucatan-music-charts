import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

# Configuración de credenciales
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

try:
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    print(f"Error de autenticación: {e}")

# LISTA DE ARTISTAS (Asegúrate de que digan 'artist' en el link)
ARTIST_IDS = [
    '0I2Tq9Hq752Y1b8YF1Fm3x', # Armando Manzanero
    '3YfS898Vf6SWH7I0NfbnIu', # Aleks Syntek
    '5KAtp7K4IStTclXhCidW9m', # Los Baby's
]

def get_artist_data():
    artists_list = []
    
    print(f"Iniciando búsqueda de {len(ARTIST_IDS)} IDs...")

    for artist_id in ARTIST_IDS:
        try:
            # Pedimos los datos a Spotify
            artist = sp.artist(artist_id)
            
            # Extraemos la información básica
            info = {
                "Nombre": artist['name'],
                "Seguidores": artist['followers']['total'],
                "Popularidad": artist['popularity'],
                "Link": artist['external_urls']['spotify']
            }
            artists_list.append(info)
            print(f"✅ Encontrado: {artist['name']}")
            
        except Exception as e:
            print(f"❌ Error con el ID {artist_id}: Podría ser una canción y no un artista.")

    # IMPORTANTE: Creamos el archivo aunque esté vacío para que GitHub no de error
    if len(artists_list) > 0:
        df = pd.DataFrame(artists_list)
        df = df.sort_values(by="Seguidores", ascending=False)
    else:
        # Si no hay nada, creamos una tabla de ejemplo para que no falle la web
        df = pd.DataFrame([{"Nombre": "Sin datos", "Seguidores": 0, "Popularidad": 0, "Link": ""}])
    
    df.to_csv("artistas_yucatan.csv", index=False)
    print("💾 Proceso finalizado. Archivo guardado.")

if __name__ == "__main__":
    get_artist_data()
