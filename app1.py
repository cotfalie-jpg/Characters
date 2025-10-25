import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="OCR Vision Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos CSS con tema tecnológico oscuro
st.markdown("""
<style>
    /* Fondo principal con gradiente tecnológico */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Header principal con efecto neón */
    .main-header {
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 50%, #7c4dff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Headers secundarios */
    .sub-header {
        font-size: 1.8rem;
        color: #00d4ff;
        margin-bottom: 1.5rem;
        font-weight: 700;
        border-bottom: 3px solid #00d4ff;
        padding-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    }
    
    /* Contenedor de cámara con borde glowy */
    .camera-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.2);
        border: 2px solid #00d4ff;
        background: rgba(0, 212, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Panel de configuración glassmorphism */
    .config-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Result box con efecto de cristal */
    .result-box {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        border-left: 5px solid #00d4ff;
        margin-top: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Botones modernos */
    .stButton button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
        color: #0f0f23;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.5);
        background: linear-gradient(135deg, #0099ff 0%, #00d4ff 100%);
    }
    
    /* Radio buttons personalizados */
    .stRadio > div {
        flex-direction: row;
        gap: 15px;
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stRadio label {
        font-weight: 600;
        color: #ffffff !important;
        font-size: 1rem;
    }
    
    /* Dividers con efecto glowy */
    .divider {
        border-top: 2px solid rgba(0, 212, 255, 0.3);
        margin: 2rem 0;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.1);
    }
    
    /* Text area personalizado */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        font-family: 'Courier New', monospace !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2) !important;
    }
    
    /* Métricas personalizadas */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Info box */
    .info-box {
        background: rgba(0, 212, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 212, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Spinner personalizado */
    .stSpinner > div {
        border-color: #00d4ff transparent transparent transparent !important;
    }
    
    /* Ajustes generales de texto */
    .stMarkdown, .stText, .stLabel {
        color: #ffffff !important;
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
        border-radius: 10px;
    }
    
    /* Efectos de hover en contenedores */
    .config-box:hover, .result-box:hover {
        border-color: rgba(0, 212, 255, 0.5);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">🔍 OCR APP</h1>', unsafe_allow_html=True)

# Crear columnas para el diseño
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h1 class="sub-header">CAPTURA DE IMAGEN</h1>', unsafe_allow_html=True)
    
    # Contenedor para la cámara con estilo tecnológico
    with st.container():
        img_file_buffer = st.camera_input("Toma una foto para analizar el texto", label_visibility="collapsed")

with col2:
    st.markdown('<h2 class="sub-header">⚙️ CONFIGURACIÓN</h2>', unsafe_allow_html=True)
    
    # Panel de configuración estilo glassmorphism
    with st.container():
        st.markdown('<div class="config-box">', unsafe_allow_html=True)
        st.markdown("### 🎛️ MODO DE PROCESAMIENTO")
        filtro = st.radio(
            "Selecciona el modo de procesamiento:",
            ('Con Filtro', 'Sin Filtro'),
            help="El filtro invierte los colores para mejorar la detección en texto claro sobre fondo oscuro"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 💡 INSTRUCCIONES")
        st.markdown("""
        **1.** 📸 Captura una imagen nítida del texto  
        **2.** ⚙️ Selecciona el modo de filtro apropiado  
        **3.** 📝 El texto detectado aparecerá automáticamente  
        
        **💡 Tip:** Usa 'Con Filtro' para texto claro sobre fondos oscuros
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Procesamiento de la imagen
if img_file_buffer is not None:
    # Mostrar indicador de procesamiento
    with st.spinner('🔄 PROCESANDO IMAGEN - ANALIZANDO TEXTO...'):
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
    st.markdown('<h2 class="sub-header">📄 TEXTO DETECTADO</h2>', unsafe_allow_html=True)
    
    if text.strip():
        # Contenedor estilizado para el texto resultante
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        
        # Mostrar estadísticas rápidas
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("🔤 Caracteres", len(text))
        with col_stats2:
            st.metric("📝 Palabras", len(text.split()))
        with col_stats3:
            st.metric("📊 Líneas", len(text.split('\n')))
        
        st.text_area("**TEXTO EXTRAÍDO:**", text, height=250, key="texto_extraido")
        
        # Botón para copiar texto
        if st.button("📋 COPIAR TEXTO AL PORTAPAPELES"):
            st.code(text)
            st.success("✅ ¡Texto copiado exitosamente!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("""
        ❌ **NO SE DETECTÓ TEXTO EN LA IMAGEN** 
        
        **Posibles soluciones:**
        - Asegúrate de que el texto esté bien enfocado y iluminado
        - Prueba alternando entre los modos de filtro
        - Verifica que haya suficiente contraste entre texto y fondo
        - Acerca más la cámara al texto
        - Intenta con una imagen más nítida
        """)

# Pie de página tecnológico
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style='
        text-align: center; 
        color: #00d4ff; 
        margin-top: 2rem; 
        padding: 2rem; 
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        backdrop-filter: blur(10px);
    '>
        <div style='font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;'>
            🚀 OCR VISION PRO
        </div>
        <div style='color: rgba(255, 255, 255, 0.8);'>
            Powered by Streamlit • OpenCV • Tesseract OCR
        </div>
        <div style='color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin-top: 0.5rem;'>
            Tecnología de vanguardia para reconocimiento de texto
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)
