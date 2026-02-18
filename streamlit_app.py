import streamlit as st
import re # Usaremos Expresiones Regulares para limpiar el HTML

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="Match Center Pro", page_icon="⚽", layout="centered")

st.markdown("""
<style>
    /* Estilos Generales */
    .modern-card {
        background-color: #ffffff;
        color: #31333F; /* Texto oscuro forzado */
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
        "eventos": [{"min": "17'", "texto": "Gol Koke", "lado": "local", "icono": "⚽"}]
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
# 3. HELPER FUNCTION (LA SOLUCIÓN CLAVE)
# ==========================================
def clean_html(raw_html):
    """
    Esta función elimina saltos de línea y espacios excesivos entre etiquetas.
    Evita que Markdown interprete la indentación como bloques de código.
    """
    # Elimina saltos de línea
    clean = raw_html.replace("\n", "")
    # Elimina espacios múltiples entre etiquetas (opcional pero recomendado)
    clean = re.sub(r'>\s+<', '><', clean)
    return clean

# ==========================================
# 4. RENDERIZADO
# ==========================================

def render_match_card(partido):
    # Escribimos el HTML legible en el código, pero lo pasamos por clean_html
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
    
    # IMPORTANTE: Aquí aplicamos la limpieza
    st.markdown(clean_html(html_structure), unsafe_allow_html=True)

    # Expander de eventos
    if partido['eventos']:
        with st.expander("Ver detalles"):
            for ev in partido['eventos']:
                st.write(f"{ev['min']} - {ev['icono']} {ev['texto']}")

# ==========================================
# 5. EJECUCIÓN
# ==========================================
st.title("Resultados")
for p in partidos:
    render_match_card(p)