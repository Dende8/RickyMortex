import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="RickyMortex", page_icon="icon.png", layout="wide")

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def ver_ficha(personaje_id):
    st.session_state.personaje_seleccionado = personaje_id
    st.session_state.tab_activa = "Ficha"

def on_tab_change():
    pass  # no necesitas hacer nada aquí, solo activa el seguimiento de estado

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
solo_unknown = st.sidebar.checkbox("Unknown")
total_epsd = st.sidebar.slider("Total de episodios", 0, int(df["n_episodes"].max()), 0, 1)

f = df.copy()

if "personaje_seleccionado" not in st.session_state:
    st.session_state.personaje_seleccionado = None

if busca:
    f = f[f["name"].str.contains(busca, case=False, na=False)] #case=False para que no distinga mayúsculas de minúsculas, na=False para que no de error con los valores nulos
if sel_especie:
    f = f[f["species"].isin(sel_especie)]
estados_seleccionados = []
if solo_vivos:
    estados_seleccionados.append("Alive")
if solo_muertos:
    estados_seleccionados.append("Dead")
if solo_unknown:
    estados_seleccionados.append("unknown")
if estados_seleccionados:  # si al menos uno está marcado
    f = f[f["status"].isin(estados_seleccionados)]
f = f[f["n_episodes"] >= total_epsd]

tab_inicio, tab_dex, tab_ficha, tab_stats = st.tabs(["Inicio", "RickyMortex", "Ficha", "Estadísticas"], on_change=on_tab_change, key="tab_activa")

with tab_inicio:
    # f""" ... """ -> f-string multilínea: {len(df)} se sustituye por el número real (151, 386...)
    # -> el texto se adapta solo si cambias N. unsafe_allow_html=True para que pinte el HTML del banner.
    st.markdown(f"""
    <div class="hero">
      <h1><img src="data:image/png;base64,{icon_b64_rick}" width="100" style="vertical-align:middle; border-radius:50%; margin-right:8px"><img src="data:image/png;base64,{icon_b64_morty}" width="100" style="vertical-align:middle; border-radius:50%; margin-right:8px"> RickyMortex</h1>
      <p>Los {len(df)} personajes de Rick y Morty · datos de rickandmortyapi.com · hecho con Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


# CSS de las tarjetas — solo se ejecuta una vez
st.markdown("""
<style>
div[class*="st-key-card_"] {
    border: 1px solid rgba(140,140,160,0.15);
    border-radius: 14px;
    padding: 12px 10px 8px;
    transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
div[class*="st-key-card_"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    border-color: rgba(140,140,160,0.45);
}
div[class*="st-key-card_"] button {
    background: transparent !important;
    border: none !important;
    color: #999 !important;
    font-size: 0.78rem !important;
    padding: 2px 0 !important;
    width: 100%;
}
div[class*="st-key-card_"] button:hover {
    color: #fff !important;
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

with tab_dex:
    if not len(f):
        st.warning("No se encontraron personajes con esos filtros.")
    else:
        n_cols = 6

        vista = f.sort_values("id").head(len(f))
        cols = st.columns(n_cols)

        for i, (_, p) in enumerate(vista.iterrows()):
            with cols[i % n_cols]:
                with st.container(key=f"card_{p['id']}"):
                    st.image(p["image"], width=110)
                    st.write(f"**{int(p['id']):03d} - {p['name']}**")
                    st.button("Ver ficha →", key=f"btn_{p['id']}",
                               on_click=ver_ficha, args=(p["id"],))

with tab_ficha:
    if st.session_state.personaje_seleccionado is None:
        st.info("Selecciona un personaje en la pestaña RickyMortex.")
    else:
        p = df[df["id"] == st.session_state.personaje_seleccionado].iloc[0]
        st.image(p["image"], width=200)
        st.subheader(p["name"])
        st.write(f"**Estado:** {p['status']}")
        st.write(f"**Especie:** {p['species']}")
        st.write(f"**Tipo:** {p['type']}")
        st.write(f"**Género:** {p['gender']}")
        st.write(f"**Origen:** {p['origin']}")
        st.write(f"**Ubicación:** {p['location']}")
        st.write(f"**Episodios:** {p['n_episodes']}")

with tab_stats:
    st.subheader("Estado de los personajes")

    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]

    fig_status = px.pie(
        status_counts, names="status", values="count", hole=0.45,
        color="status",
        color_discrete_map={"Alive": "#4CAF50", "Dead": "#E53935", "unknown": "#9E9E9E"}
    )
    st.plotly_chart(fig_status, use_container_width=True)

    st.subheader("Especies más comunes")

    species_counts = df["species"].value_counts()
    top_species = species_counts.head(10).reset_index()
    top_species.columns = ["species", "count"]

    fig_species = px.bar(
        top_species, x="count", y="species", orientation="h"
    )
    fig_species.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_species, use_container_width=True)

    st.subheader("Origen y ubicación")
    col1, col2 = st.columns(2)

with col1:
    origin_counts = df[df["origin"] != "unknown"]["origin"].value_counts().head(10).reset_index()
    origin_counts.columns = ["origin", "count"]
    fig_origin = px.bar(
           origin_counts, x="count", y="origin", orientation="h",
        title="Top 10 lugares de origen"
    )
    fig_origin.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_origin, use_container_width=True)

with col2:
    location_counts = df[df["location"] != "unknown"]["location"].value_counts().head(10).reset_index()
    location_counts.columns = ["location", "count"]
    fig_location = px.bar(
        location_counts, x="count", y="location", orientation="h",
        title="Top 10 ubicaciones"
    )
    fig_location.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_location, use_container_width=True)