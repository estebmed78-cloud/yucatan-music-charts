import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

# Credenciales
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# IDs DE ARTISTAS (Asegúrate de que sean de Artista, no de Canción)
ARTIST_IDS = [
    '0r8toju2ecKaVtItkzAnNi', # Aleks Syntek
    '5lODCkFdEtpPn3YxfmyLfT', # Armando Manzanero
    '1XXNhXjfbtXeW1amhbUKIW', # Guty Cárdenas
    '7DU6GDSRD6R2Jp47MHVBoZ', # Ricardo Palmerín
    '1rOKqpRUdTI1LQm1JSC9Fq', # Pepe Domínguez
    '1Mxy1ynui2eF5RTGSuf8zz', # Sergio Esquivel
    '0i5xphNVjZjYKhBrgpwEvl', # Frank Dominguez
    '2VF3Q0THbnB66J0XqsTnvs', # Las Trovadoras del Mayab
    '5aZIISGJbYHpXa48fdtVu2', # Orquesta Jaranera Sonora Yucateca
    '2G2XaGpCLB6u7Zze4G0b2Z', # Trío Los Condes de Yucatán
    '5S6I6Hf8alD1pZZMuh3Msx', # Trío Los Duendes del Mayab
    '3hMkukzp8Zx9ru8YyT3xWv', # Rondalla Miramar
    '5mRcujdcqi9Fd0BMRglkdX', # Paleto La Voz De La Cumbia
    '390JqAY27HgXFLnmFM0TUQ', # Cleyver y La Nueva Imagen
    '4nfZ8OQwyrQMDLSpHK6D3u', # Los Master's
    '5RLbaO6vu3wyo06gAMxAQh', # Francely Abreuu
    '60FYZ0x5u10Z9oTq6hJW7j', # FREEKIDS
    '4Sel9suIpjL2glt946Fx4I', # Kafi
    '6Y6PSJtk4jYnPsIvEY9rR0', # María San Felipe
    '0NMcMJSS44FeZd4WTjIWWm', # Mafud
    '4JTbF9feswVonYL7fHSVCh', # Valeria Jasso
    '7w2LEbH35jdB5RamMTuf40', # Pat Boy
    '6PM7WHmPauW14UWFRVHn4A', # Acid Waves
    '6QjG9UpVwNY2cVYzrK7rzk', # King Wong
    '4G4obTj9Zrn43Xy6NIN3MW', # Ruben Arias
    '5BuGRexAfSNpAvv4sdTSSG', # Nano el Cenzontle
    '6ele7BTJO8pRXTdsiSYfPI', # Azul Ciego
    '0pbaMVXuQlnvgBAZC5O633', # Evverest
    '3zkA2PRX69BOCl90INvvay', # Lejo
    '6X5rGZg2cu2ohGh1KCY31W', # ARALIIA
    '0ytX6A2k1vxamhfNuTXXMz', # Pedro Honda
    '5Hv87Mn4SDQwoETOZ9PtXD', # Dary Alva
    '37owCqnfmM5jO9QWCQbc2u', # Moon Jungle
    '0If5A5XvlWopqFC8Iz4nUy', # JETLAG
    '3otlAvVRLjmlSjCNDA8SBu', # Yaalen K'uj
    '0LyhUzhNljm28MWW1rqdPx', # Val Hozu
    '02BFiwJ2Lobf8GCaEOeKoF', # Alice True Colors
    '768RzQlCnAdXhP77CzbDOb', # Barzoo
    '0jg1se3iGMLanXUpvQqsL4', # Jairo Zubieta
    '6DVPqGk0KYbHvNCl2M8Rib', # Cecilio Perera
    '28IQ11zdFruEbyD6mfNTkT', # Mr. Bliss
    '3fOJ22606VnkMcK4HcCLxw', # Alfredo Ávila
    '0hQEpgP4edbDkFiSJkI8Ns', # Danyisra
    '6fF05Jq6daFXZIk1EFmp08', # Jerry Velázquez
    '2v6HDzecSuTKO4difHVJJp', # Orquesta del Mayab
    '1ELq4iGndnnomb2dpys8ej', # Los Juglares
    '7jhzu3iGN5BGNEcBWkT8GC', # flxbabu
    '2PJ4Op1XxwdFwv9azSLElN', # Lu Esperón
    '01EGp5MWcP7jRNOUAKBmZr', # Montejo
    # Agrega aquí tus otros IDs...
]

def get_artist_data():
    artists_list = []
    
    for artist_id in ARTIST_IDS:
        try:
            # Intentamos obtener la info del artista
            artist = sp.artist(artist_id)
            
            # Verificamos si tiene la información que necesitamos
            if 'followers' in artist:
                artists_list.append({
                    "Nombre": artist['name'],
                    "Seguidores": artist.get('followers', {}).get('total', 0),
                    "Popularidad": artist.get('popularity', 0),
                    "Género": ", ".join(artist.get('genres', [])[:2]),
                    "Link": artist.get('external_urls', {}).get('spotify', '')
                })
                print(f"✅ Éxito: {artist['name']}")
            else:
                print(f"⚠️ El ID {artist_id} no parece ser de un artista (no tiene seguidores).")
                
        except Exception as e:
            print(f"❌ Error con el ID {artist_id}: {e}")
    
    # Si logramos obtener al menos un artista, guardamos el archivo
    if artists_list:
        df = pd.DataFrame(artists_list)
        df = df.sort_values(by="Seguidores", ascending=False)
        df.to_csv("artistas_yucatan.csv", index=False)
        print(f"💾 ¡Archivo guardado con {len(artists_list)} artistas!")
    else:
        # Creamos un archivo vacío para que GitHub Actions no de error de "archivo no encontrado"
        pd.DataFrame(columns=["Nombre","Seguidores"]).to_csv("artistas_yucatan.csv", index=False)
        print("⚠️ No se encontró ningún artista válido, se creó un archivo vacío.")

if __name__ == "__main__":
    get_artist_data()
