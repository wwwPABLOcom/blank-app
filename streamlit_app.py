import streamlit as st
import textwrap

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="Match Center Pro", page_icon="⚽", layout="centered")

# CSS ARREGLADO:
# 1. Se fuerza el color de texto 'color: #31333F' dentro de la tarjeta.
# 2. Se eliminan espacios raros y se asegura la jerarquía.
st.markdown("""
<style>
    /* Contenedor principal de la tarjeta */
    .modern-card {
        background-color: #ffffff;
        color: #31333F !important; /* <--- CRUCIAL: Fuerza texto oscuro sobre fondo blanco */
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        font-family: sans-serif;
    }
    
    /* Etiqueta de Fecha */
    .date-badge {
        background-color: #f0f2f6;
        color: #555;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        margin-bottom: 12px;
    }

    /* Contenedores Flexbox */
    .match-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }

    .team-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        width: 30%; /* Ancho fijo relativo */
    }
    
    .team-logo {
        font-size: 3rem;
        margin-bottom: 8px;
        line-height: 1;
    }
    
    .team-name {
        font-weight: 700;
        font-size: 1rem;
        text-align: center;
        line-height: 1.2;
        color: #000000; /* Aseguramos negro puro */
    }
    
    .score-box {
        text-align: center;
        width: 40%;
    }

    .score-display {
        font-size: 3rem;
        font-weight: 800;
        color: #1a1a1a;
        line-height: 1;
        letter-spacing: -1px;
    }
    
    .match-status {
        color: #ff4b4b;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Línea de tiempo */
    .timeline-min {
        font-weight: bold;
        color: #888;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATOS
# ==========================================
partidos = [
    {
        "id": 1,
        "fecha_corta": "SAB 13.12",
        "hora": "14:00",
        "local": {"nombre": "Atlético", "escudo": "🔴⚪"},
        "visitante": {"nombre": "Valencia", "escudo": "🦇"},
        "marcador": "2 - 1",
        "estado": "FINAL",
        "eventos": [
            {"min": "17'", "texto": "Gol de Koke", "lado": "local", "icono": "⚽"},
            {"min": "32'", "texto": "Amarilla a Pubill", "lado": "local", "icono": "🟨"},
            {"min": "55'", "texto": "Cambio: Entra Beltrán", "lado": "visitante", "icono": "🔄"},
            {"min": "88'", "texto": "Gol de Hugo Duro", "lado": "visitante", "icono": "⚽"},
        ]
    },
    {
        "id": 2,
        "fecha_corta": "VIE 12.12",
        "hora": "21:00",
        "local": {"nombre": "R. Sociedad", "escudo": "🔵⚪"},
        "visitante": {"nombre": "Girona FC", "escudo": "🔴⚪"},
        "marcador": "1 - 2",
        "estado": "FINAL",
        "eventos": []
    }
]

# ==========================================
# 3. LÓGICA DE RENDERIZADO
# ==========================================

def render_match_card(partido):
    # Usamos textwrap.dedent para limpiar la indentación y evitar 
    # que Markdown lo interprete como bloque de código.
    # Además, usamos clases CSS limpias.
    html_code = textwrap.dedent(f"""
        <div class="modern-card">
            <div style="text-align: center;">
                <span class="date-badge">
                    📅 {partido['fecha_corta']} • ⏰ {partido['hora']}
                </span>
            </div>
            
            <div class="match-header">
                <div class="team-container">
                    <div class="team-logo">{partido['local']['escudo']}</div>
                    <div class="team-name">{partido['local']['nombre']}</div>
                </div>

                <div class="score-box">
                    <div class="score-display">{partido['marcador']}</div>
                    <div class="match-status">{partido['estado']}</div>
                </div>

                <div class="team-container">
                    <div class="team-logo">{partido['visitante']['escudo']}</div>
                    <div class="team-name">{partido['visitante']['nombre']}</div>
                </div>
            </div>
        </div>
    """)
    
    st.markdown(html_code, unsafe_allow_html=True)

    # Expander nativo de Streamlit
    with st.expander("Ver detalles", expanded=False):
        if partido['eventos']:
            st.caption("Minuto a Minuto")
            for evento in partido['eventos']:
                c1, c2, c3 = st.columns([5, 2, 5])
                
                # HTML inline simple para alineación
                if evento['lado'] == 'local':
                    c1.markdown(f"<div style='text-align:right; font-size:0.9rem'><b>{evento['texto']}</b> {evento['icono']}</div>", unsafe_allow_html=True)
                    c2.markdown(f"<div style='text-align:center; color:#888; font-weight:bold; font-size:0.8rem'>{evento['min']}</div>", unsafe_allow_html=True)
                else:
                    c2.markdown(f"<div style='text-align:center; color:#888; font-weight:bold; font-size:0.8rem'>{evento['min']}</div>", unsafe_allow_html=True)
                    c3.markdown(f"<div style='text-align:left; font-size:0.9rem'>{evento['icono']} <b>{evento['texto']}</b></div>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 1px; background-color: #f0f0f0; margin: 5px 0;'></div>", unsafe_allow_html=True)
        else:
            st.info("Sin incidencias destacables.")

# ==========================================
# 4. APP PRINCIPAL
# ==========================================

st.title("🏆 Resultados LaLiga")

# Debugging rápido: Si esto no sale, el problema es de Python, no de CSS
if not partidos:
    st.error("No hay datos cargados.")

for p in partidos:
    render_match_card(p)