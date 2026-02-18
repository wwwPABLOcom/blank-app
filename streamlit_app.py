import streamlit as st
import pandas as pd
from datetime import date

# Configuración de la página
st.set_page_config(page_title="Academia Los Centellas", layout="wide")

# 1. SIMULACIÓN DE BASE DE DATOS (Se reinicia al recargar la página)
if 'datos_partidos' not in st.session_state:
    # Datos iniciales inventados
    data = [
        {"Fecha": date(2023, 10, 12), "Categoría": "Sub-12 A", "Rival": "Leones del Norte", "Goles Favor": 3, "Goles Contra": 1, "Estado": "Jugado"},
        {"Fecha": date(2023, 10, 19), "Categoría": "Sub-14 B", "Rival": "Rayo Vallecano", "Goles Favor": 2, "Goles Contra": 2, "Estado": "Jugado"},
        {"Fecha": date(2023, 11, 5),  "Categoría": "Sub-16 A", "Rival": "Dragones City", "Goles Favor": 0, "Goles Contra": 0, "Estado": "Pendiente"},
        {"Fecha": date(2023, 11, 12), "Categoría": "Sub-12 A", "Rival": "Escuela Municipal", "Goles Favor": 0, "Goles Contra": 0, "Estado": "Pendiente"},
    ]
    st.session_state.datos_partidos = pd.DataFrame(data)

# Función para cargar datos
def cargar_datos():
    return st.session_state.datos_partidos

# 2. BARRA LATERAL (Navegación)
st.sidebar.image("https://img.icons8.com/color/96/football2.png", width=100)
st.sidebar.title("Navegación")
modo = st.sidebar.radio("Ir a:", ["📅 Calendario y Resultados", "🔒 Área de Entrenadores"])

st.title("⚽ Academia de Fútbol 'Los Centellas'")

# ---------------------------------------------------------
# VISTA 1: CALENDARIO PÚBLICO (Solo lectura)
# ---------------------------------------------------------
if modo == "📅 Calendario y Resultados":
    st.subheader("Próximos Encuentros y Últimos Resultados")
    
    df = cargar_datos()
    
    # Filtros para los padres
    col1, col2 = st.columns(2)
    with col1:
        filtro_cat = st.multiselect("Filtrar por Categoría:", df["Categoría"].unique())
    
    # Aplicar filtro si se selecciona algo
    if filtro_cat:
        df_mostrar = df[df["Categoría"].isin(filtro_cat)]
    else:
        df_mostrar = df

    # Separar jugados de pendientes
    jugados = df_mostrar[df_mostrar["Estado"] == "Jugado"].sort_values(by="Fecha", ascending=False)
    pendientes = df_mostrar[df_mostrar["Estado"] == "Pendiente"].sort_values(by="Fecha")

    tab1, tab2 = st.tabs(["🏆 Resultados", "📆 Próximos Partidos"])

    with tab1:
        if not jugados.empty:
            # Mostrar como tabla estilizada
            st.dataframe(
                jugados,
                column_config={
                    "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
                    "Goles Favor": st.column_config.NumberColumn("GF", help="Goles a Favor"),
                    "Goles Contra": st.column_config.NumberColumn("GC", help="Goles en Contra"),
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No hay partidos jugados con este filtro.")

    with tab2:
        if not pendientes.empty:
            st.dataframe(
                pendientes[["Fecha", "Categoría", "Rival"]],
                column_config={
                    "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.success("¡No hay partidos pendientes! A entrenar.")

# ---------------------------------------------------------
# VISTA 2: ADMIN (Edición)
# ---------------------------------------------------------
elif modo == "🔒 Área de Entrenadores":
    st.subheader("Gestión de Partidos (Modo Editor)")
    
    # Simulamos un login muy básico
    password = st.sidebar.text_input("Contraseña de Admin", type="password")
    
    if password == "gol123":  # Contraseña inventada
        st.success("Acceso concedido. Modo edición activado.")
        
        st.markdown("""
        **Instrucciones:**
        * Haz doble clic en cualquier celda para editar (resultado, fecha, rival).
        * Usa la última fila vacía para **añadir** un partido nuevo.
        * Selecciona filas y pulsa 'Suprimir' para borrar.
        """)

        df_editor = st.session_state.datos_partidos

        # WIDGET PODEROSO: Data Editor
        # Permite editar el dataframe como si fuera un Excel
        df_editado = st.data_editor(
            df_editor,
            num_rows="dynamic", # Permite añadir filas
            column_config={
                "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
                "Estado": st.column_config.SelectboxColumn(
                    "Estado",
                    options=["Pendiente", "Jugado", "Aplazado"],
                    required=True
                ),
                "Categoría": st.column_config.SelectboxColumn(
                    "Categoría",
                    options=["Sub-10", "Sub-12 A", "Sub-12 B", "Sub-14 A", "Sub-14 B", "Sub-16 A"],
                    required=True
                ),
                "Goles Favor": st.column_config.NumberColumn("GF", min_value=0, max_value=20, step=1),
                "Goles Contra": st.column_config.NumberColumn("GC", min_value=0, max_value=20, step=1),
            },
            hide_index=True,
            use_container_width=True,
            key="editor_partidos"
        )

        # Guardar cambios
        # En Streamlit, el data_editor actualiza el estado, pero aquí forzamos la asignación
        # para asegurarnos de que la vista pública vea los cambios inmediatamente.
        if not df_editado.equals(st.session_state.datos_partidos):
            st.session_state.datos_partidos = df_editado
            st.rerun() # Recargar la página para ver cambios reflejados
            
    else:
        if password:
            st.error("Contraseña incorrecta.")
        st.warning("Introduce la contraseña en la barra lateral para editar.")