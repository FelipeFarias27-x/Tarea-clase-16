import streamlit as st

st.set_page_config(page_title="BiciDatos", layout="wide")

if "df" not in st.session_state:
    st.session_state["df"] = None
if "tipo_usuario" not in st.session_state:
    st.session_state["tipo_usuario"] = "Todos"
if "tipo_dia" not in st.session_state:
    st.session_state["tipo_dia"] = "Todos"
if "rango_horas" not in st.session_state:
    st.session_state["rango_horas"] = (0, 23)

pg_explorar = st.Page("page_explorar.py", title="Explorar los datos", default=True)
pg_comparar = st.Page("page_comparar.py", title="Comparar horarios")

pg = st.navigation([pg_explorar, pg_comparar])

with st.sidebar:
    st.title("BiciDatos")
    st.divider()
    
    st.session_state["tipo_usuario"] = st.selectbox(
        "Tipo de usuario",
        options=["Todos", "Ocasionales", "Registrados"],
        index=["Todos", "Ocasionales", "Registrados"].index(st.session_state["tipo_usuario"])
    )
    
    st.session_state["tipo_dia"] = st.radio(
        "Tipo de día",
        options=["Todos", "Laborable", "No laborable"],
        index=["Todos", "Laborable", "No laborable"].index(st.session_state["tipo_dia"])
    )
    
    st.session_state["rango_horas"] = st.slider(
        "Horas del día",
        min_value=0,
        max_value=23,
        value=st.session_state["rango_horas"]
    )

def obtener_datos_filtrados():
    df = st.session_state["df"]
    if df is None:
        return None
    
    df_filtrado = df.copy()
    
    if st.session_state["tipo_dia"] != "Todos":
        df_filtrado = df_filtrado[df_filtrado["tipo_dia"] == st.session_state["tipo_dia"]]
        
    h_min, h_max = st.session_state["rango_horas"]
    df_filtrado = df_filtrado[(df_filtrado["hora"] >= h_min) & (df_filtrado["hora"] <= h_max)]
    
    usuario = st.session_state["tipo_usuario"]
    if usuario == "Todos":
        df_filtrado["alquileres"] = df_filtrado["alquileres_total"]
    elif usuario == "Ocasionales":
        df_filtrado["alquileres"] = df_filtrado["alquileres_ocasionales"]
    else:
        df_filtrado["alquileres"] = df_filtrado["alquileres_registrados"]
        
    return df_filtrado

st.session_state["filtrar_datos"] = obtener_datos_filtrados

pg.run()
