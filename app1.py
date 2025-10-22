import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="OCR App",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .sidebar .sidebar-content {
        background-color: #F8FAFC;
    }
    .stRadio > div {
        flex-direction: row;
        align-items: center;
    }
    .stRadio > label {
        font-weight: 500;
    }
    .result-box {
        background-color: #F0F9FF;
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 5px solid #3B82F6;
        margin-top: 2rem;
    }
    .camera-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .divider {
        border-top: 2px solid #E2E8F0;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">Reconocimiento Óptico de Caracteres</h1>', unsafe_allow_html=True)

# Crear columnas para el diseño
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2 class="sub-header">Captura de Imagen</h2>', unsafe_allow_html=True)
    
    # Contenedor para la cámara con estilo
    with st.container():
        st.markdown('<div class="camera-container">', unsafe_allow_html=True)
        img_file_buffer = st.camera_input("Toma una foto para analizar el texto")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h2 class="sub-header">⚙️ Configuración</h2>', unsafe_allow_html=True)
    
    # Sidebar dentro de la columna
    with st.container():
        st.markdown("### Filtros de Procesamiento")
        filtro = st.radio(
            "Selecciona el modo de procesamiento:",
            ('Con Filtro', 'Sin Filtro'),
            help="El filtro invierte los colores de la imagen para mejorar la detección de texto en algunos casos"
        )
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        st.markdown("### Información")
        st.info("""
        **Instrucciones:**
        1. Toma una foto del texto que deseas analizar
        2. Selecciona si aplicar filtro o no
        3. El texto detectado aparecerá automáticamente
        """)

# Procesamiento de la imagen
if img_file_buffer is not None:
    # Mostrar indicador de procesamiento
    with st.spinner('Procesando imagen y detectando texto...'):
        # To read image file buffer with OpenCV:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        
        # Aplicar filtro si es necesario
        if filtro == 'Con Filtro':
            cv2_img = cv2.bitwise_not(cv2_img)
        
        # Convertir a RGB para Tesseract
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        
        # Realizar OCR
        text = pytesseract.image_to_string(img_rgb)
    
    # Mostrar resultados
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Texto Detectado</h2>', unsafe_allow_html=True)
    
    if text.strip():
        # Contenedor estilizado para el texto resultante
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.text_area("Texto extraído:", text, height=200, key="texto_extraido")
        
        # Botón para copiar texto
        if st.button("Copiar Texto"):
            st.code(text)
            st.success("¡Texto copiado al portapapeles!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No se detectó texto en la imagen. Intenta con otra imagen o ajusta el filtro.")

# Pie de página
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #64748B; margin-top: 2rem;'>"
    "Aplicación de OCR desarrollada con Streamlit | "
    "Usando OpenCV y Tesseract OCR"
    "</div>", 
    unsafe_allow_html=True
)
