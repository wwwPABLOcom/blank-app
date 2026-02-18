import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS (CSS)
# ==========================================
st.set_page_config(page_title="Match Center Pro", page_icon="⚽", layout="centered")

st.markdown("""
<style>
    /* Estilo para la tarjeta principal */
    .modern-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
    }
    
    /* Contenedor Flex para alinear equipos y marcador */
    .match-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }

    /* Estilos del Equipo */
    .team-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 30%; /* Ancho fijo para centrar */
    }
    .team-logo {
        font-size: 3rem; /* Escudos grandes */
        margin-bottom: 8px;
    }
    .team-name {
        font-weight: 700;
        font-size: 1rem;
        color: #333;
        text-align: center;
    }

    /* Estilos del Marcador Central */
    .score-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 40%;
    }
    .score-val {
        font-size: 2.8rem; /* Marcador MUY grande */
        font-weight: 800;
        color: #1a1a1a;
        line-height: 1;
        letter-spacing: -1px;
    }
    .match-meta {
        background-color: #f1f3f5;
        color: #555;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 10px;
        border: 1px solid #ddd;
    }
    .match-status {
        color: #ff4b4b; /* Rojo para FINAL */
        font-size: 0.7rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    /* Línea de tiempo simple */
    .timeline-row {
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
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
        "fecha": "SAB 13.12",
        "hora": "14:00",
        "local": {"nombre": "Atlético", "escudo": "🔴⚪"},
        "visitante": {"nombre": "Valencia", "escudo": "🦇"},
        "marcador": "2 - 1",
        "estado": "FINAL",
        "eventos": [
            {"min": "17'", "texto": "Gol de Koke", "lado": "local", "icono": "⚽"},
            {"min": "32'", "texto": "Amarilla Pubill", "lado": "local", "icono": "🟨"},
            {"min": "55'", "texto": "Entra Beltrán", "lado": "visitante", "icono": "🔄"},
             {"min": "88'", "texto": "Gol Hugo Duro", "lado": "visitante", "icono": "⚽"},
        ]
    },
    {
        "id": 2,
        "fecha": "VIE 12.12",
        "hora": "21:00",
        "local": {"nombre": "R. Sociedad", "escudo": "🔵⚪"},
        "visitante": {"nombre": "Girona FC", "escudo": "🔴⚪"},
        "marcador": "1 - 2",
        "estado": "FINAL",
        "eventos": []
    }
]

# ==========================================
# 3. FUNCIÓN DE RENDERIZADO (CORREGIDA)
# ==========================================

def render_match_card(partido):
    # IMPORTANTE: El string HTML está pegado a la izquierda (sin espacios al inicio)
    # para evitar que Markdown lo interprete como bloque de código.
    html_structure = f"""
<div class="modern-card">
    <div class="match-content">
        <div class="team-box">
            <div class="team-logo">{partido['local']['escudo']}</div>
            <div class="team-name">{partido['local']['nombre']}</div>
        </div>

        <div class="score-box">
            <div class="match-status">{partido['estado']}</div>
            <div class="score-val">{partido['marcador']}</div>
            <div class="match-meta">
                📅 {partido['fecha']} &nbsp;|&nbsp; ⏰ {partido['hora']}
            </div>
        </div>

        <div class="team-box">
            <div class="team-logo">{partido['visitante']['escudo']}</div>
            <div class="team-name">{partido['visitante']['nombre']}</div>
        </div>
    </div>
</div>
"""
    # Renderizamos el HTML
    st.markdown(html_structure, unsafe_allow_html=True)

    # Botón/Expander para ver detalles (Fuera del HTML puro para funcionalidad nativa)
    with st.expander("Ver detalles del partido", expanded=False):
        if partido['eventos']:
            for evento in partido['eventos']:
                c1, c2, c3 = st.columns([4, 1, 4])
                
                # Alineación de eventos (Local izq, Visitante der)
                if evento['lado'] == 'local':
                    c1.markdown(f"<div style='text-align:right'><b>{evento['texto']}</b> {evento['icono']}</div>", unsafe_allow_html=True)
                    c2.markdown(f"<div style='text-align:center; color:#888; font-weight:bold'>{evento['min']}</div>", unsafe_allow_html=True)
                else:
                    c2.markdown(f"<div style='text-align:center; color:#888; font-weight:bold'>{evento['min']}</div>", unsafe_allow_html=True)
                    c3.markdown(f"<div style='text-align:left'>{evento['icono']} <b>{evento['texto']}</b></div>", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 0; border: 0; border-top: 1px dashed #eee;'>", unsafe_allow_html=True)
        else:
            st.caption("No hay eventos registrados.")

# ==========================================
# 4. APP PRINCIPAL
# ==========================================

st.title("🏆 Resultados LaLiga")
st.write("") # Espacio

for p in partidos:
    render_match_card(p)