import streamlit as st
import pandas as pd
import altair as alt

st.header("Explorar los datos")

archivo = st.file_uploader("Selecciona bicicletas_listas.csv", type=["csv"])

if st.button("Cargar datos"):
    if archivo is not None:
        df_cargado = pd.read_csv(archivo, sep=",", encoding="utf-8-sig", parse_dates=["fecha"])
        st.session_state["df"] = df_cargado
        st.success(f"{len(df_cargado):,} registros cargados.".replace(",", "."))
    else:
        st.warning("Por favor, selecciona primero el archivo bicicletas_listas.csv.")

if st.session_state["df"] is None:
    st.info("Instrucción: Sube el archivo `bicicletas_listas.csv` y pulsa **Cargar datos** para comenzar.")
    st.stop()

df_filtrado = st.session_state["filtrar_datos"]()

col1, col2 = st.columns(2)
total_alquileres = int(df_filtrado["alquileres"].sum())
promedio_hora = df_filtrado["alquileres"].mean() if len(df_filtrado) > 0 else 0.0

with col1:
    st.metric("Total de alquileres", f"{total_alquileres:,}".replace(",", "."))
with col2:
    st.metric("Promedio por hora observada", f"{promedio_hora:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."))

tab_grafico, tab_datos = st.tabs(["Gráfico diario", "Datos"])

with tab_grafico:
    diario = df_filtrado.groupby("fecha", as_index=False)["alquileres"].sum()
    
    chart = alt.Chart(diario).mark_line(color="#197A8D").encode(
        x=alt.X("fecha:T", title="Fecha"),
        y=alt.Y("alquileres:Q", title="Alquileres por día"),
        tooltip=["fecha:T", "alquileres:Q"]
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    st.caption("Cada total incluye las horas que conservan los filtros.")

with tab_datos:
    df_mostrar = df_filtrado.copy()
    df_mostrar["fecha"] = df_mostrar["fecha"].dt.strftime("%Y-%m-%d")
    
    st.dataframe(df_mostrar, use_container_width=True)
    
    csv_descarga = df_mostrar.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="Descargar datos filtrados",
        data=csv_descarga,
        file_name="bicicletas_filtradas.csv",
        mime="text/csv"
    )
    
    st.markdown("Fanaee-T, H. (2013). Bike Sharing [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894. Licencia CC BY 4.0.")
    
    st.link_button(
        label="Consultar la fuente en UCI",
        url="https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset"
    )
