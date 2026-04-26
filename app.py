import streamlit as st
import pandas as pd

st.set_page_config(page_title="YucaCharts", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    th { background-color: #1DB954 !important; color: white !important; }
    </style>
    """, unsafe_allow_all_headers=True)

st.title("Yucatán Music Chart")
st.caption("Actualizado diariamente con datos reales de Spotify")

try:
    df = pd.read_csv("artistas_yucatan.csv")
    
    # Formatear números con comas para que sea legible
    df_display = df[['Nombre', 'Listeners', 'Daily', 'Peak']].copy()
    
    # Función para poner color al Daily +/-
    def color_daily(val):
        color = 'green' if val > 0 else 'red' if val < 0 else 'black'
        return f'color: {color}; font-weight: bold'

    st.dataframe(
        df_display.style.applymap(color_daily, subset=['Daily']),
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.warning("Esperando la primera actualización de datos... (Ejecuta el Scraper en GitHub)")
