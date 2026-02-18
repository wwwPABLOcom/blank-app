import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS MODERNOS (CSS)
# ==========================================
st.set_page_config(page_title="Match Center Pro", page_icon="⚽", layout="centered")

# Inyectamos CSS avanzado para el estilo "Big & Modern"
st.markdown("""
<style>
    /* Contenedor principal de la tarjeta */
    .modern-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #f0f0f0;
    }
    
    /* Etiqueta de Fecha y Hora (Optimizando espacio) */
    .date-badge {
        background-color: #f8f9fa;
        color: #666;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid #eee;
    }

    /* Estilos de los equipos y marcador */
    .team-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100px;
    }
    .team-logo {
        font-size: 3.5rem; /* Escudos GIGANTES */
        margin-bottom: 5px;
    }
    .team-name {
        font-weight: 700;
        font-size: 1rem;
        text-align: center;
        line-height: 1.2;
    }
    
    .score-display {
        font-size: 3.5rem; /* Marcador GIGANTE */
        font-weight: 800;
        color: #1a1a1a;
        margin: 0 20px;
        letter-spacing: -2px;
    }
    
    .match-status {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 0.8rem;
        text-transform: uppercase;
        margin-top: -10px;
    }

    /* Línea de tiempo vertical limpia */
    .timeline-item {
        padding: 8px 0;
        border-bottom: 1px dashed #eee;
    }
    .timeline-min {
        font-weight: bold;
        color: #888;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATOS (Simulados)
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
        "local": {"nombre": "Real Sociedad", "escudo": "🔵⚪"},
        "visitante": {"nombre": "Girona FC", "escudo": "🔴⚪"},
        "marcador": "1 - 2",
        "estado": "FINAL",
        "eventos": []
    }
]

# ==========================================
# 3. COMPONENTES VISUALES
# ==========================================

def render_match_card(partido):
    # Creamos un contenedor HTML personalizado para el encabezado
    # La corrección está aquí: el HTML está pegado a la izquierda (sin espacios)
    html_header = f"""
<div class="modern-card">
    <div style="text-align: center;">
        <span class="date-badge">
            📅 {partido['fecha_corta']} &nbsp;|&nbsp; ⏰ {partido['hora']}
        </span>
    </div>
    
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
        <div class="team-container">
            <div class="team-logo">{partido['local']['escudo']}</div>
            <div class="team-name">{partido['local']['nombre']}</div>
        </div>

        <div style="text-align: center;">
            <div class="score-display">{partido['marcador']}</div>
            <div class="match-status">{partido['estado']}</div>
        </div>

        <div class="team-container">
            <div class="team-logo">{partido['visitante']['escudo']}</div>
            <div class="team-name">{partido['visitante']['nombre']}</div>
        </div>
    </div>
</div>
"""
    
    st.markdown(html_header, unsafe_allow_html=True)

    # Usamos un expander invisible (sin label visible) o un botón para ver detalles
    # En este caso, usaremos un expander limpio debajo de la tarjeta visual
    with st.expander("Ver detalles del partido", expanded=False):
        if partido['eventos']:
            st.markdown("##### ⏱️ Minuto a Minuto")
            for evento in partido['eventos']:
                # Lógica visual para alinear eventos a izq o der
                col1, col2, col3 = st.columns([4, 1, 4])
                
                if evento['lado'] == 'local':
                    with col1: st.markdown(f"<div style='text-align:right'><b>{evento['texto']}</b> {evento['icono']}</div>", unsafe_allow_html=True)
                    with col2: st.markdown(f"<div style='text-align:center' class='timeline-min'>{evento['min']}</div>", unsafe_allow_html=True)
                else:
                    with col2: st.markdown(f"<div style='text-align:center' class='timeline-min'>{evento['min']}</div>", unsafe_allow_html=True)
                    with col3: st.markdown(f"<div style='text-align:left'>{evento['icono']} <b>{evento['texto']}</b></div>", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 5px 0; border-top: 1px dashed #eee;'>", unsafe_allow_html=True)
        else:
            st.info("No hay eventos registrados para este partido.")

# ==========================================
# 4. APP
# ==========================================

st.markdown("## 🏆 LaLiga EA Sports")
st.markdown("Resultados en vivo y estadísticas")
st.write("") # Espaciador

for p in partidos:
    render_match_card(p)