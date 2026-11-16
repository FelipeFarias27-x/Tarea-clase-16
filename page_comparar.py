import streamlit as st
import altair as alt

st.header("Comparar horarios")

if st.session_state["df"] is None:
    st.info("Instrucción: Ve a la página **Explorar los datos**, sube `bicicletas_listas.csv` y pulsa **Cargar datos** para comenzar.")
    st.stop()

df_filtrado = st.session_state["filtrar_datos"]()

color_barras = st.color_picker("Color de las barras", value="#197A8D")

promedios_hora = df_filtrado.groupby("hora", as_index=False)["alquileres"].mean()
promedios_hora.rename(columns={"alquileres": "promedio"}, inplace=True)

chart_barras = alt.Chart(promedios_hora).mark_bar(color=color_barras).encode(
    x=alt.X("hora:O", title="Hora del día", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("promedio:Q", title="Alquileres por hora observada"),
    tooltip=[
        alt.Tooltip("hora:O", title="Hora"),
        alt.Tooltip("promedio:Q", title="Promedio", format=".1f")
    ]
)

st.altair_chart(chart_barras, use_container_width=True)

if st.checkbox("Mostrar tabla de promedios"):
    tabla_mostrar = promedios_hora.copy()
    tabla_mostrar["promedio"] = tabla_mostrar["promedio"].round(2)
    st.dataframe(tabla_mostrar, use_container_width=True, hide_index=True)

st.divider()

limite = st.number_input(
    "Límite de alquileres por hora",
    min_value=0,
    value=250,
    step=10
)

horas_superan = promedios_hora[promedios_hora["promedio"] > limite]["hora"].tolist()
total_horas_con_datos = len(promedios_hora)

st.metric(
    label="Horarios con promedio mayor que el límite",
    value=f"{len(horas_superan)}/{total_horas_con_datos}"
)

if horas_superan:
    horarios_formateados = ", ".join(f"{int(h):02d}:00" for h in sorted(horas_superan))
    st.write(f"**Horarios:** {horarios_formateados}.")
else:
    st.write("**Horarios:** Ningún horario supera el límite seleccionado.")
