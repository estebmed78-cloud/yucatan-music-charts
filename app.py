import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Yucatán Artist Chart (Spotify)")

try:
    df = pd.read_csv("artistas_yucatan.csv")
    
    # Formatear números con comas para que se vea profesional
    df['Listeners'] = df['Listeners'].apply(lambda x: f"{x:,}")
    df['Peak'] = df['Peak'].apply(lambda x: f"{x:,}")
    
    # Colorear el Daily +/- (Verde si es positivo, rojo si es negativo)
    def color_daily(val):
        color = 'green' if val > 0 else 'red' if val < 0 else 'gray'
        return f'color: {color}'

    st.table(df[['Nombre', 'Listeners', 'Daily', 'Peak']])

except:
    st.error("No hay datos todavía. Ejecuta el scraper en GitHub Actions.")
