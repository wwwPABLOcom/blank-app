import streamlit as st
import re # Necesario para la limpieza del HTML

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="Match Center Pro", page_icon="⚽", layout="centered")

st.markdown("""
<style>
    /* Estilos Generales */
    .modern-card {
        background-color: #ffffff;
        color: #31333F; /* Texto oscuro forzado para evitar modo oscuro invisible */
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        font-family: sans-serif;
    }
    
    .date-badge {
        background-color: #f0f2f6;
        color: #555;
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 15px;
        display: inline-block;
    }

    /* Flexbox para el header */
    .match-header {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }

    .team-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 30%;
    }
    
    .team-logo { font-size: 3rem; margin-bottom: 5px; }
    .team-name { font-weight: 700; font-size: 1rem; text-align: center; }
    
    .score-box { text-align: center; width: 40%; }
    .score-display { font-size: 3rem; font-weight: 800; line-height: 1; }
    .match-status { color: #ff4b4b; font-weight: 700; font-size: 0.8rem; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATOS (AHORA CUADRAN PERFECTAMENTE)
# ==========================================
partidos = [
    {
        "id": 1,
        "fecha_corta": "SAB 13.12",
        "hora": "14:00",
        "local": {"nombre": "Atlético", "escudo": "🔴⚪"},
        "visitante": {"nombre": "Valencia", "escudo": "🦇"},
        "marcador": "2 - 1", # Resultado Final
        "estado": "FINAL",
        "eventos": [
            # Goles: 2 para Local, 1 para Visitante
            {"min": "17'", "texto": "Gol de Koke", "lado": "local", "icono": "⚽"},
            {"min": "32'", "texto": "Amarilla a Pubill", "lado": "local", "icono": "🟨"},
            {"min": "55'", "texto": "Cambio: Entra Beltrán", "lado": "visitante", "icono": "🔄"},
            {"min": "74'", "texto": "Gol de Griezmann", "lado": "local", "icono": "⚽"}, # <--- GOL AÑADIDO
            {"min": "88'", "texto": "Gol de Hugo Duro", "lado": "visitante", "icono": "⚽"},
        ]
    },
    {
        "id": 2,
        "fecha_corta": "VIE 12.12",
        "hora": "21:00",
        "local": {"nombre": "R. Sociedad", "escudo": "🔵⚪"},
        "visitante": {"nombre": "Girona FC", "escudo": "🔴⚪"},
        "marcador": "1 - 2", # Resultado Final
        "estado": "FINAL",
        "eventos": [
            # Goles: 1 para Local, 2 para Visitante
            {"min": "22'", "texto": "Gol de Savinho", "lado": "visitante", "icono": "⚽"},
            {"min": "40'", "texto": "Lesión de Zubimendi", "lado": "local", "icono": "🚑"},
            {"min": "44'", "texto": "Gol de Kubo", "lado": "local", "icono": "⚽"},
            {"min": "65'", "texto": "Amarilla a Blind", "lado": "visitante", "icono": "🟨"},
            {"min": "89'", "texto": "Gol de Stuani", "lado": "visitante", "icono": "⚽"}, # <--- GOL DE LA VICTORIA
        ]
    }
]

# ==========================================
# 3. HELPER FUNCTION (LA SOLUCIÓN TÉCNICA)
# ==========================================
def clean_html(raw_html):
    """
    Minifica el HTML eliminando saltos de línea para evitar 
    que Markdown lo interprete como bloque de código.
    """
    clean = raw_html.replace("\n", "")
    clean = re.sub(r'>\s+<', '><', clean)
    return clean

# ==========================================
# 4. RENDERIZADO
# ==========================================

def render_match_card(partido):
    # Definimos el HTML con estructura visual clara
    html_structure = f"""
    <div class="modern-card">
        <div style="text-align: center;">
            <span class="date-badge">📅 {partido['fecha_corta']} • ⏰ {partido['hora']}</span>
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
    """
    
    # Renderizamos pasando por la limpieza
    st.markdown(clean_html(html_structure), unsafe_allow_html=True)

    # Lógica del Expander (Detalles)
    with st.expander("Ver detalles del partido", expanded=False):
        if partido['eventos']:
            st.caption("Minuto a Minuto")
            for evento in partido['eventos']:
                c1, c2, c3 = st.columns([5, 2, 5])
                
                # HTML inline simple para la línea de tiempo
                if evento['lado'] == 'local':
                    # Evento a la izquierda
                    c1.markdown(f"<div style='text-align:right; font-size:0.9rem'><b>{evento['texto']}</b> {evento['icono']}</div>", unsafe_allow_html=True)
                    c2.markdown(f"<div style='text-align:center; color:#888; font-weight:bold; font-size:0.8rem'>{evento['min']}</div>", unsafe_allow_html=True)
                else:
                    # Evento a la derecha
                    c2.markdown(f"<div style='text-align:center; color:#888; font-weight:bold; font-size:0.8rem'>{evento['min']}</div>", unsafe_allow_html=True)
                    c3.markdown(f"<div style='text-align:left; font-size:0.9rem'>{evento['icono']} <b>{evento['texto']}</b></div>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 1px; background-color: #f0f0f0; margin: 5px 0;'></div>", unsafe_allow_html=True)
        else:
            st.info("No hay eventos registrados.")

# ==========================================
# 5. EJECUCIÓN
# ==========================================
st.title("🏆 Resultados LaLiga")

for p in partidos:
    render_match_card(p)