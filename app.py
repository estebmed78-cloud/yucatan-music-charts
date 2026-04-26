import streamlit as st
import pandas as pd

st.set_page_config(page_title="Yuca Music Chart", page_icon="🎸")

st.title("🎸 Yucatán Music Chart")
st.subheader("Ranking de artistas yucatecos basado en datos de Spotify")

# Cargar los datos
try:
    df = pd.read_csv("artistas_yucatan.csv")
    
    # Mostrar el Top 1 (El más seguido)
    top_artista = df.iloc[0]
    st.metric(label="Artista #1", value=top_artista['Nombre'], delta=f"{top_artista['Seguidores']} seguidores")

    # Mostrar tabla estilizada
    st.write("### Ranking")
    st.dataframe(
        df,
        column_config={
            "Link": st.column_config.LinkColumn("Spotify Link"),
            "Popularidad": st.column_config.ProgressColumn("Popularidad", format="%d", min_value=0, max_value=100)
        },
        hide_index=True,
        use_container_width=True
    )

    # Gráfico de barras
    st.write("### Comparativa de Seguidores")
    st.bar_chart(data=df, x="Nombre", y="Seguidores")

except FileNotFoundError:
    st.error("Aún no hay datos disponibles. El scraper debe ejecutarse primero.")

st.caption("Los datos se actualizan automáticamente cada 24 horas.")
