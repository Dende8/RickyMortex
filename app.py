import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import base64

st.set_page_config(page_title="RickyMortex", page_icon="icon.png", layout="wide")

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

@st.cache_data
def cargar():
    return pd.read_csv(Path(__file__).parent / "RMcharacters.csv")

df = cargar()

icon_b64_rick = get_base64_image("rick.png")
icon_b64_morty = get_base64_image("morty.png")

st.sidebar.title("Búsqueda y filtros")
busca = st.sidebar.text_input("Busca por nombre", placeholder="Ejemplo: Morty Smith")
sel_especie = st.sidebar.multiselect("Especie", sorted(df["species"].dropna().unique()))
solo_vivos = st.sidebar.checkbox("Vivos")
solo_muertos = st.sidebar.checkbox("Muertos")
total_epsd = st.sidebar.slider("Total de episodios", 0, int(df["n_episodes"].max()), 0, 1)

f = df.copy()
if busca:
    f = f[f["name"].str.contains(busca, case=False, na=False)] #case=False para que no distinga mayúsculas de minúsculas, na=False para que no de error con los valores nulos
if sel_especie:
    f = f[f["type_1"].isin(sel_especie)]
if solo_vivos:
    f = f[f["status"] == "Alive"]
if solo_muertos:
    f = f[f["status"] == "Dead"]
f = f[f["n_episodes"] >= total_epsd]

tab_inicio, tab_dex= st.tabs(["Inicio", "RickyMortex"])

with tab_inicio:
    # f""" ... """ -> f-string multilínea: {len(df)} se sustituye por el número real (151, 386...)
    # -> el texto se adapta solo si cambias N. unsafe_allow_html=True para que pinte el HTML del banner.
    st.markdown(f"""
    <div class="hero">
      <h1><img src="data:image/png;base64,{icon_b64_rick}" width="100" style="vertical-align:middle; border-radius:50%; margin-right:8px"><img src="data:image/png;base64,{icon_b64_morty}" width="100" style="vertical-align:middle; border-radius:50%; margin-right:8px"> RickyMortex</h1>
      <p>Los {len(df)} personajes de Rick y Morty · datos de rickandmortyapi.com · hecho con Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
