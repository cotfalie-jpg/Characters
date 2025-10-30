import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# -------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------------------------------------
st.set_page_config(
    page_title="BAE OCR 💛",
    page_icon="🍼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# ESTILOS VISUALES — ESTILO BAE 🌼
# -------------------------------------------------------
st.markdown("""
<style>
    /* Fondo general pastel */
    [data-testid="stAppViewContainer"] {
        background-color: #FFF8EA;
        color: #3C3C3C;
        font-family: 'Poppins', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #FFF2C3;
        border-right: 2px solid #DD8E6B30;
    }

    /* Encabezados principales */
    h1, h2, h3 {
        color: #DD8E6B;
        font-weight: 700;
    }

    .main-header {
        text-align: center;
        font-size: 3rem;
        color: #DD8E6B;
        margin-top: 0.5em;
    }

    /* Contenedores con efecto suave */
    .glass-box {
        background-color: #FFFFFFCC;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0px 4px 20px rgba(221,142,107,0.15);
        border: 1px solid #DD8E6B25;
    }

    /* Botones */
    .stButton > button {
        background-color: #C6E2E3;
        color: #3C3C3C;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6em 1.2em;
        transition: all 0.3s ease;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
    }

    .stButton > button:hover {
        background-color: #DD8E6B;
        color: white;
        transform: scale(1.03);
    }

    /* Áreas de texto */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #DD8E6B40 !important;
        background-color: #FFFFFF !important;
        color: #3C3C3C !important;
    }

    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #DD8E6B !important;
        font-weight: 700;
    }

    /* Separador */
    .divider {
        border-top: 2px solid #DD8E6B20;
        margin: 2rem 0;
    }

    /* Scroll suave */
    ::-webkit-scrollbar-thumb {
        background-color: #DD8E6B50;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# INTERFAZ PRINCIPAL
# -------------------------------------------------------
st.image("logo_bae.png", width=140)
st.markdown('<h1 class="main-header">🍼 OCR con BAE</h1>', unsafe_allow_html=True)
st.write("Convierte imágenes en texto con un toque cálido y humano 🌷")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📸 Captura tu imagen")
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    img_file_buffer = st.camera_input("Toma una foto para analizar el texto", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### ⚙️ Configuración")
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    filtro = st.radio(
        "Modo de procesamiento:",
        ('Con filtro', 'Sin filtro'),
        help="Usa 'Con filtro' si el texto es claro sobre fondo oscuro."
    )
    st.markdown("""
    **Instrucciones:**
    1. Toma una imagen enfocada del texto.  
    2. Selecciona el modo adecuado según el fondo.  
    3. Presiona para procesar y ver el texto detectado 💛
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# PROCESAMIENTO DE LA IMAGEN
# -------------------------------------------------------
if img_file_buffer is not None:
    with st.spinner("💛 Analizando tu imagen..."):
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        if filtro == 'Con filtro':
            cv2_img = cv2.bitwise_not(cv2_img)

        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📄 Texto detectado")

    if text.strip():
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        colA, colB, colC = st.columns(3)
        with colA:
            st.metric("🔤 Caracteres", len(text))
        with colB:
            st.metric("📝 Palabras", len(text.split()))
        with colC:
            st.metric("📊 Líneas", len(text.split('\n')))

        st.text_area("Texto extraído:", text, height=250, key="texto_extraido")

        if st.button("💾 Copiar texto"):
            st.code(text)
            st.success("Texto copiado exitosamente 💛")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ No se detectó texto. Prueba con más luz o mejor enfoque.")

# -------------------------------------------------------
# PIE DE PÁGINA
# -------------------------------------------------------
st.markdown("---")
st.markdown("✨ Desarrollado con amor por **BAE | IA afectiva** 💛")

