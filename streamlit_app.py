import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS UX
# ==========================================
st.set_page_config(page_title="Match Center", page_icon="⚽", layout="centered")

# Inyectamos CSS para mejorar la legibilidad visual (Tipografía y espaciado)
st.markdown("""
<style>
    .match-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #ff4b4b;
    }
    .score-box {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        background-color: white;
        padding: 5px 15px;
        border-radius: 5px;
        border: 1px solid #e0e0e0;
    }
    .team-name {
        font-size: 18px;
        font-weight: 600;
    }
    .event-minute {
        font-weight: bold;
        color: #555;
    }
    /* Alineación de eventos */
    .event-home { text-align: right; padding-right: 10px; border-right: 2px solid #ddd; }
    .event-away { text-align: left; padding-left: 10px; border-left: 2px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ESTRUCTURA DE DATOS (MODELO)
# ==========================================
# Usamos una estructura rica para manejar cualquier tipo de evento
partidos = [
    {
        "id": 1,
        "fecha": "SAB 13.12.2025",
        "hora": "14:00",
        "local": {"nombre": "Atlético de Madrid", "corto": "ATM", "escudo": "🛡️"}, # Emoji como placeholder
        "visitante": {"nombre": "Valencia CF", "corto": "VAL", "escudo": "🦇"},
        "marcador": {"local": 2, "visitante": 1},
        "estado": "Finalizado",
        "eventos": [
            {"min": 17, "tipo": "gol", "equipo": "local", "jugador": "Koke", "icono": "⚽"},
            {"min": 32, "tipo": "tarjeta", "equipo": "local", "jugador": "Marc Pubill", "icono": "🟨"},
            {"min": 42, "tipo": "tarjeta", "equipo": "local", "jugador": "Sørloth", "icono": "🟨"},
            {"min": 46, "tipo": "cambio", "equipo": "local", "entra": "Le Normand", "sale": "Molina", "icono": "🔄"},
            {"min": 55, "tipo": "cambio", "equipo": "visitante", "entra": "Beltrán", "sale": "Diego López", "icono": "🔄"},
            {"min": 88, "tipo": "gol", "equipo": "visitante", "jugador": "Hugo Duro", "icono": "⚽"}, # Evento extra para demo
        ]
    },
    {
        "id": 2,
        "fecha": "VIE 12.12.2025",
        "hora": "21:00",
        "local": {"nombre": "Real Sociedad", "corto": "RSO", "escudo": "🔵"},
        "visitante": {"nombre": "Girona FC", "corto": "GIR", "escudo": "🔴"},
        "marcador": {"local": 1, "visitante": 2},
        "estado": "Finalizado",
        "eventos": [] # Sin datos detallados
    }
]

# ==========================================
# 3. COMPONENTES DE UI (VISTA)
# ==========================================

def render_timeline(eventos):
    """Renderiza una línea de tiempo vertical (Mejor UX para móviles que la horizontal)"""
    if not eventos:
        st.info("No hay detalles minuto a minuto disponibles.")
        return

    # Ordenar eventos por minuto
    eventos_sorted = sorted(eventos, key=lambda x: x['min'])

    st.markdown("### ⏱️ Minuto a Minuto")
    
    for evento in eventos_sorted:
        c1, c2, c3 = st.columns([5, 1, 5])
        
        texto_evento = f"**{evento.get('jugador', '')}**"
        if evento['tipo'] == 'cambio':
            texto_evento = f"<span style='color:green'>In: {evento['entra']}</span><br><span style='color:red; font-size:0.8em'>Out: {evento['sale']}</span>"
        
        # Lógica de renderizado: Izquierda (Local) o Derecha (Visitante)
        if evento['equipo'] == 'local':
            with c1:
                st.markdown(f"<div class='event-home'>{texto_evento} {evento['icono']}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='text-align:center' class='event-minute'>{evento['min']}'</div>", unsafe_allow_html=True)
        else:
            with c2:
                st.markdown(f"<div style='text-align:center' class='event-minute'>{evento['min']}'</div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='event-away'>{evento['icono']} {texto_evento}</div>", unsafe_allow_html=True)

def render_match_header(partido):
    """Renderiza la tarjeta resumen del partido"""
    # Usamos columnas para centrar el marcador
    col_local, col_score, col_visit = st.columns([3, 2, 3])
    
    with col_local:
        st.markdown(f"<div style='text-align:right'><h2>{partido['local']['escudo']}</h2><div class='team-name'>{partido['local']['nombre']}</div></div>", unsafe_allow_html=True)
    
    with col_score:
        st.markdown(f"<br><div class='score-box'>{partido['marcador']['local']} - {partido['marcador']['visitante']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-size:0.8em; color:gray'>{partido['estado']}</div>", unsafe_allow_html=True)
        
    with col_visit:
        st.markdown(f"<div style='text-align:left'><h2>{partido['visitante']['escudo']}</h2><div class='team-name'>{partido['visitante']['nombre']}</div></div>", unsafe_allow_html=True)

# ==========================================
# 4. APP PRINCIPAL
# ==========================================

st.title("⚽ LaLiga | Match Center")
st.markdown("**Jornada 16** | Temporada 2025/2026")
st.divider()

# Iterar sobre los partidos
for p in partidos:
    # Contenedor visual para cada partido
    with st.container():
        # Cabecera pequeña con fecha
        st.caption(f"📅 {p['fecha']} | ⏰ {p['hora']}")
        
        # Usamos Expander pero personalizado para que actúe como el "acordeón" de la imagen
        # El label del expander está vacío o minimalista, y metemos el contenido visual dentro
        with st.expander(f"{p['local']['corto']} vs {p['visitante']['corto']} ({p['marcador']['local']}-{p['marcador']['visitante']})", expanded=(p['id']==1)):
            
            # 1. Cabecera visual del partido (Escudos y Goles grandes)
            render_match_header(p)
            
            st.divider()
            
            # 2. Línea de tiempo (El detalle clave de la imagen)
            render_timeline(p['eventos'])
            
            # 3. Estadísticas extra (Opcional, mejora la UX)
            if p['eventos']:
                st.caption("Goles: ⚽ | Tarjetas: 🟨 🟥 | Cambios: 🔄")