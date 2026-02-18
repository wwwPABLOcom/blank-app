import streamlit as st

# ==========================================
# 1. DATOS DE EJEMPLO (Reemplazar con datos reales)
# ==========================================
# Lista de partidos con su información básica y detalles opcionales
partidos_jornada = [
    {
        "fecha": "VIE 12.12.2025", "hora": "21:00", "balon": "⚽",
        "local": "REAL SOCIEDAD", "escudo_local": "🔵⚪",
        "resultado": "1-2",
        "visitante": "GIRONA FC", "escudo_visitante": "🔴⚪",
        "detalles": [] # Sin detalles
    },
    {
        "fecha": "SAB 13.12.2025", "hora": "14:00", "balon": "⚽",
        "local": "ATLÉTICO DE MADRID", "escudo_local": "🔴⚪",
        "resultado": "2-1",
        "visitante": "VALENCIA CF", "escudo_visitante": "🦇",
        "detalles": [ # Lista de eventos para el detalle del partido
            {"minuto": "17'", "equipo": "local", "tipo": "gol", "jugador": "KOKE", "icono": "⚽"},
            {"minuto": "32'", "equipo": "local", "tipo": "tarjeta", "jugador": "MARC PUBILL", "icono": "🟨"},
            {"minuto": "42'", "equipo": "local", "tipo": "tarjeta", "jugador": "SØRLOTH", "icono": "🟨"},
            {"minuto": "46'", "equipo": "local", "tipo": "cambio", "jugador_entra": "LE NORMAND", "jugador_sale": "MOLINA", "icono": "🔄"},
            {"minuto": "55'", "equipo": "visitante", "tipo": "cambio", "jugador_entra": "BELTRÁN", "jugador_sale": "DIEGO LÓPEZ", "icono": "🔄"},
        ]
    },
    {
        "fecha": "SAB 13.12.2025", "hora": "16:15", "balon": "⚽",
        "local": "RCD MALLORCA", "escudo_local": "👹",
        "resultado": "3-1",
        "visitante": "ELCHE CF", "escudo_visitante": "🌴",
        "detalles": []
    },
    # ... añadir el resto de partidos siguiendo la misma estructura
]

# ==========================================
# 2. FUNCIONES DE VISUALIZACIÓN
# ==========================================

def mostrar_detalle_partido(partido):
    """Muestra la línea de tiempo de eventos de un partido."""
    with st.container():
        # Usamos columnas para la estructura: Escudo Local | Línea de Tiempo | Escudo Visitante
        col_escudo_l, col_timeline, col_escudo_v = st.columns([1, 4, 1])

        with col_escudo_l:
            st.markdown(f"<h1 style='text-align: center;'>{partido['escudo_local']}</h1>", unsafe_allow_html=True)

        with col_timeline:
            # Línea de tiempo horizontal (simulada con una barra de progreso)
            st.progress(100) 
            
            # Iterar sobre los eventos y mostrarlos debajo de la línea
            for evento in partido["detalles"]:
                # Crear columnas para cada evento para alinearlos horizontalmente
                cols_evento = st.columns(len(partido["detalles"])) # Tantas columnas como eventos
                
                # Encontrar la columna correspondiente al evento actual
                # (Esto es una simplificación, una implementación real calcularía la posición por minuto)
                indice_evento = partido["detalles"].index(evento)
                col_actual = cols_evento[indice_evento]

                with col_actual:
                    st.markdown(f"<div style='text-align: center; font-weight: bold;'>{evento['minuto']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center;'>{evento['icono']}</div>", unsafe_allow_html=True)
                    
                    # Mostrar información del jugador(es)
                    if evento['tipo'] == 'cambio':
                         st.markdown(f"<div style='text-align: center; font-size: 0.8em;'>{evento['jugador_entra']}</div>", unsafe_allow_html=True)
                         st.markdown(f"<div style='text-align: center; font-size: 0.8em; color: gray;'>{evento['jugador_sale']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: center; font-size: 0.8em;'>{evento['jugador']}</div>", unsafe_allow_html=True)
                        
                    # Indicar con una flecha si es del equipo local o visitante
                    if evento['equipo'] == 'local':
                        st.markdown(f"<div style='text-align: center;'>⬆️</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: center;'>⬇️</div>", unsafe_allow_html=True)

        with col_escudo_v:
             st.markdown(f"<h1 style='text-align: center;'>{partido['escudo_visitante']}</h1>", unsafe_allow_html=True)


def mostrar_fila_partido(partido, index):
    """Muestra la fila resumen de un partido."""
    # Crear un contenedor expandible para cada partido
    with st.expander(label="", expanded=False):
        # Cabecera del expansor (la fila del partido)
        # Usamos columnas para alinear los elementos como en la imagen
        col_fecha, col_hora, col_balon, col_partido = st.columns([1.5, 1, 1, 4])

        with col_fecha:
            st.write(f"**{partido['fecha']}**")
        
        with col_hora:
            st.write(f"**{partido['hora']}**")
        
        with col_balon:
            st.write(f"{partido['balon']}")
        
        with col_partido:
            # Sub-columnas para el detalle del enfrentamiento
            c_local, c_esc_l, c_res, c_esc_v, c_visit = st.columns([2, 0.5, 1, 0.5, 2])
            with c_local: st.write(f"**{partido['local']}**")
            with c_esc_l: st.write(f"{partido['escudo_local']}")
            with c_res: st.markdown(f"<div style='text-align: center; font-weight: bold; color: red;'>{partido['resultado']}</div>", unsafe_allow_html=True)
            with c_esc_v: st.write(f"{partido['escudo_visitante']}")
            with c_visit: st.write(f"**{partido['visitante']}**")

        # Contenido del expansor (los detalles del partido)
        # Se muestra solo si hay detalles definidos para el partido
        if partido["detalles"]:
            mostrar_detalle_partido(partido)
        else:
            st.info("No hay detalles disponibles para este partido.")

# ==========================================
# 3. APLICACIÓN PRINCIPAL
# ==========================================

# Configuración de la página
st.set_page_config(page_title="Jornada 16 | LaLiga", layout="wide")

# Título principal
st.markdown("## 📅 **JORNADA 16 | 2025/2026**")

# Cabecera de la tabla
col_h_fecha, col_h_hora, col_h_balon, col_h_partido = st.columns([1.5, 1, 1, 4])
col_h_fecha.markdown("**FECHA**")
col_h_hora.markdown("**HORARIO**")
col_h_balon.markdown("**BALÓN**")
col_h_partido.markdown("**PARTIDO**")
st.divider() # Línea separadora

# Bucle principal para mostrar cada partido
for i, partido in enumerate(partidos_jornada):
    mostrar_fila_partido(partido, i)