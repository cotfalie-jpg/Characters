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

# Aplicar estilos CSS personalizados mejorados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4F46E5;
        margin-bottom: 1rem;
        font-weight: 600;
        border-bottom: 2px solid #E0E7FF;
        padding-bottom: 0.5rem;
    }
    .sidebar .sidebar-content {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .stRadio > div {
        flex-direction: row;
        align-items: center;
        gap: 10px;
    }
    .stRadio > label {
        font-weight: 500;
        color: #374151;
    }
    .result-box {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #3B82F6;
        margin-top: 2rem;
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.1);
    }
    .camera-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px -8px rgba(59, 130, 246, 0.3);
        border: 2px solid #E0F2FE;
    }
    .divider {
        border-top: 2px solid #E2E8F0;
        margin: 1.5rem 0;
    }
    .config-box {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    .info-box {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #10B981;
    }
    .copy-button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .copy-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    .stButton button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">🔍 Reconocimiento Óptico de Caracteres</h1>', unsafe_allow_html=True)

# Crear columnas para el diseño
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2 class="sub-header">📷 Captura de Imagen</h2>', unsafe_allow_html=True)
    
    # Contenedor para la cámara con estilo
    with st.container():
        st.markdown('<div class="camera-container">', unsafe_allow_html=True)
        img_file_buffer = st.camera_input("Toma una foto para analizar el texto", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h2 class="sub-header">⚙️ Configuración</h2>', unsafe_allow_html=True)
    
    # Panel de configuración estilizado
    with st.container():
        st.markdown('<div class="config-box">', unsafe_allow_html=True)
        st.markdown("### 🎛️ Filtros de Procesamiento")
        filtro = st.radio(
            "Selecciona el modo de procesamiento:",
            ('Con Filtro', 'Sin Filtro'),
            help="El filtro invierte los colores de la imagen para mejorar la detección de texto en algunos casos"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 💡 Información")
        st.markdown("""
        **Instrucciones:**
        1. 📸 Toma una foto del texto
        2. ⚙️ Selecciona el modo de filtro
        3. 📝 El texto aparecerá automáticamente
        
        **Consejo:** Usa "Con Filtro" para texto claro sobre fondo oscuro
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Procesamiento de la imagen
if img_file_buffer is not None:
    # Mostrar indicador de procesamiento
    with st.spinner('🔄 Procesando imagen y detectando texto...'):
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
    st.markdown('<h2 class="sub-header">📄 Texto Detectado</h2>', unsafe_allow_html=True)
    
    if text.strip():
        # Contenedor estilizado para el texto resultante
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        
        # Mostrar estadísticas rápidas
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("Caracteres", len(text))
        with col_stats2:
            st.metric("Palabras", len(text.split()))
        with col_stats3:
            st.metric("Líneas", len(text.split('\n')))
        
        st.text_area("**Texto extraído:**", text, height=200, key="texto_extraido")
        
        # Botón para copiar texto
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("📋 Copiar Texto", use_container_width=True):
                st.code(text)
                st.success("✅ ¡Texto copiado al portapapeles!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("""
        ❌ No se detectó texto en la imagen. 
        
        **Sugerencias:**
        - Asegúrate de que el texto esté bien enfocado
        - Prueba con el otro modo de filtro
        - Verifica que haya suficiente contraste
        - Acerca más la cámara al texto
        """)

# Pie de página
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #64748B; margin-top: 2rem; padding: 1.5rem; background: #F8FAFC; border-radius: 10px;'>"
    "🛠️ Aplicación de OCR desarrollada con Streamlit | "
    "Usando OpenCV y Tesseract OCR"
    "</div>", 
    unsafe_allow_html=True
)
