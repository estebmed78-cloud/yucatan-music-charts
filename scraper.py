import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

# Configuración de credenciales (las tomaremos de variables de entorno)
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Lista de IDs de artistas yucatecos (puedes añadir más buscando su ID en Spotify)
# Ejemplo: https://open.spotify.com/artist/6P7U36ZUnp9vYv0999_ID -> El ID es lo último
ARTIST_IDS = [
    '1Xyo4u3uXC1Z7oTnz4pY3U', # Aleks Syntek
    '3m9S10i4I2S7XW2fB6zC3O', # Los Juglares
    '7pYpYtS8Y9YjT4z0pXo1B6', # Vanessa Zamora (ejemplo)
    # Agrega aquí los IDs que quieras
]

def get_artist_data():
    artists_list = []
    for artist_id in ARTIST_IDS:
        try:
            artist = sp.artist(artist_id)
            artists_list.append({
                "Nombre": artist['name'],
                "Seguidores": artist['followers']['total'],
                "Popularidad": artist['popularity'],
                "Género": ", ".join(artist['genres'][:2]), # Los primeros 2 géneros
                "Link": artist['external_urls']['spotify']
            })
        except Exception as e:
            print(f"Error con el artista {artist_id}: {e}")
    
    df = pd.DataFrame(artists_list)
    df = df.sort_values(by="Seguidores", ascending=False)
    df.to_csv("artistas_yucatan.csv", index=False)
    print("Datos actualizados correctamente.")

if __name__ == "__main__":
    get_artist_data()
