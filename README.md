# 🛸 RickyMortex (https://rickymortex.streamlit.app/)

Aplicación web interactiva construida con **Streamlit** para explorar, filtrar y visualizar estadísticas de los personajes del universo de *Rick y Morty*, usando datos obtenidos en tiempo real desde la [API pública de Rick y Morty](https://rickandmortyapi.com).

---

## 📁 Estructura del proyecto

```
RickyMortex/
├── app.py                 # Aplicación Streamlit
├── prep_datos.ipnyb          # Script de extracción de datos vía API
├── RMcharacters.csv       # Dataset generado (se crea al ejecutar extraer_datos.py)
├── icon.png               # Icono de la pestaña del navegador
├── rick.png                # Icono usado en el banner principal
├── morty.png               # Icono usado en el banner principal
└── requirements.txt
```
---

## 🧪 Extracción de datos — `prep_datos.ipynb`

Notebook independiente que consulta la API REST de Rick y Morty y genera el archivo `RMcharacters.csv` consumido por la app.

**Qué hace:**

1. **Paginación automática.** La API devuelve los personajes en páginas; el código recorre todas siguiendo el campo `info.next` hasta que no quedan más páginas (`next = None`).
2. **Reintentos ante fallos de red.** Cada petición dispone de hasta 3 intentos con 1 segundo de espera entre ellos, ya que la API puede devolver respuestas vacías o cortes intermitentes. Si tras 3 intentos sigue fallando, se lanza un error explícito en vez de un traceback críptico.
3. **Normalización de campos:**
   - `type`: cuando la API devuelve un string vacío (caso muy frecuente), se sustituye por `"Not specified"` para evitar valores en blanco en los filtros de la app.
   - `episode_ids`: la API devuelve una lista de URLs de episodios (ej. `.../episode/28`); el script extrae solo el número final de cada URL y los guarda como un string separado por comas (ej. `"1,2,5,28"`). Este formato se eligió porque el CSV no soporta tipos lista de forma nativa — guardar una lista de Python directamente la convertiría en un string ilegible al releerla.
   - `n_episodes`: número total de episodios en los que aparece el personaje (`len(c["episode"])`).
4. **Exportación final** a `RMcharacters.csv` mediante `pandas.DataFrame.to_csv()`.

**Ejecución:**

```
Ejecutar el código de prep_datos.ipnyb
```

Genera/sobrescribe `RMcharacters.csv` con los datos más recientes de la API. No es necesario ejecutarlo de nuevo salvo que quieras refrescar el dataset.

---

## 🖥️ Aplicación — `app.py`

La interfaz se organiza en **4 pestañas**:

| Pestaña | Contenido |
|---|---|
| **Inicio** | Banner principal con iconos de Rick y Morty (incrustados en base64) y el conteo total de personajes del dataset. |
| **RickyMortex** | Cuadrícula de tarjetas (6 por fila) con la imagen, ID y nombre de cada personaje. Cada tarjeta incluye un botón **"Ver ficha →"** que abre automáticamente la pestaña *Ficha* con el detalle del personaje seleccionado. |
| **Ficha** | Vista detallada del personaje elegido: imagen, estado, especie, tipo, género, origen, ubicación y número de episodios. |
| **Estadísticas** | Visualizaciones con Plotly: gráfico de dona del estado de los personajes (Alive/Dead/unknown), barras horizontales de las 10 especies más comunes, y barras horizontales del top 10 de orígenes y ubicaciones (excluyendo `"unknown"` para no distorsionar el ranking). |

### Filtros (barra lateral)

- **Búsqueda por nombre** — coincidencia parcial, sin distinguir mayúsculas/minúsculas.
- **Especie** — selección múltiple.
- **Estado** (Vivos / Muertos / Unknown) — los checkboxes funcionan como un filtro **OR**: si marcas varios, se muestran todos los estados seleccionados combinados (no una intersección).
- **Episodios mínimos** — slider que filtra personajes con al menos ese número de apariciones.

### Detalles técnicos relevantes

- **Imágenes incrustadas en base64**: los iconos del banner se cargan desde disco y se convierten a base64 para poder insertarse directamente en el HTML del `st.markdown`, evitando depender de rutas de archivo accesibles por el navegador.
- **Navegación entre pestañas por código**: el clic en "Ver ficha" actualiza `st.session_state` y fuerza el salto a la pestaña *Ficha* gracias al parámetro `key` + `on_change` de `st.tabs` (control programático de la pestaña activa).
- **Tarjetas con efecto hover**: cada tarjeta se agrupa en un `st.container(key=...)`, y un CSS dirigido a esas claves (`div[class*="st-key-card_"]`) aplica una elevación visual al pasar el ratón, dando sensación de elemento clicable.

---

## ⚙️ Instalación

```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- `streamlit`
- `pandas`
- `plotly`
- `requests`

---

## ▶️ Uso

```
# 1. Generar el dataset (solo la primera vez, o para actualizar datos)
Ejecutar prep_datos.ipynb

# 2. Lanzar la aplicación
streamlit run app.py
```

---

## 🙌 Créditos

Datos obtenidos de la API pública [rickandmortyapi.com](https://rickandmortyapi.com). Proyecto desarrollado con Python y Streamlit.

