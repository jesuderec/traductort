import streamlit as st
from config.settings import settings
from core.file_handler import FileHandler
from core.translator import LiteraryTranslator
import logging
from core.text_processor import TextProcessor

logger = logging.getLogger(__name__)

def setup_streamlit():
    st.set_page_config(
        page_title="Traductor Literario Profesional",
        page_icon="📖",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
        /* Estilos personalizados para el tema oscuro */
        .stButton > button {
            background-color: #FF4B4B !important;
            color: white !important;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #A32828 !important;
        }

        .stExpander, .stStatus {
            border-color: #262730 !important;
            background-color: #12141A !important;
        }

        .stText {
            font-family: monospace;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #FF4B4B;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("✒️ Traductor Literario Profesional")
    st.markdown("""
    <div style="text-align: center; border-bottom: 1px solid #262730; padding-bottom: 20px; margin-bottom: 30px; color: #ADADAD;">
        <i>Traducciones que respetan la voz del autor, recursos estilísticos y esencia literaria</i>
    </div>
    """, unsafe_allow_html=True)
    logger.info("Interfaz de Streamlit configurada.")

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuración de Traducción")

        source_language = st.selectbox(
            "Idioma del texto original:",
            ("Auto detectar", "Español", "Inglés", "Francés", "Alemán"),
            index=0, # 'Auto detectar' por defecto
            help="Selecciona el idioma de origen del documento"
        )

        target_language = st.selectbox(
            "Traducir a:",
            ("Español", "Inglés", "Francés", "Alemán"),
            index=0, # 'Español' por defecto
            help="Selecciona el idioma de destino para la traducción"
        )

        model_choice = st.selectbox(
            "Selecciona el modelo de traducción:",
            list(settings.MODELS.keys()),
            index=0,
            help="DeepSeek para prosa general, GPT-4 para poesía y textos complejos, Mixto para máxima fidelidad"
        )

        st.markdown("---")

        with st.expander("Opciones Avanzadas", expanded=False):
            preserve_special = st.checkbox(
                "Conservar elementos especiales", 
                value=False, # <-- Valor corregido a False
                help="Mantener epígrafes, notas al pie, formatos especiales"
            )
            cultural_notes = st.checkbox(
                "Añadir notas culturales", 
                value=False, # <-- Valor corregido a False
                help="Incluir explicaciones entre [ ] para referencias culturales"
            )
        
        st.markdown("---")
        st.info("""
        **Instrucciones:**
        1. Sube tu documento (PDF, DOCX, TXT)
        2. Selecciona modelo de traducción
        3. Selecciona los idiomas de origen y destino
        4. Inicia la traducción
        5. Descarga el resultado conservando el estilo literario
        """)

        return model_choice, source_language, target_language, preserve_special, cultural_notes

def main_ui():
    setup_streamlit()
    model_choice, source_language, target_language, preserve_special, cultural_notes = render_sidebar()

    uploaded_file = st.file_uploader(
        "Sube tu obra literaria",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False
    )

    if uploaded_file:
        try:
            original_content = FileHandler.read_file(uploaded_file)

            # Detectar el idioma si se selecciona 'Auto detectar'
            if source_language == "Auto detectar":
                detected_lang_code = TextProcessor.detect_language(original_content)
                if detected_lang_code:
                    source_language = {"en": "Inglés", "es": "Español", "fr": "Francés", "de": "Alemán"}.get(detected_lang_code, "Inglés")
                    st.info(f"Idioma de origen detectado: **{source_language}**")
                else:
                    st.warning("No se pudo detectar el idioma de origen, se usará 'Inglés' por defecto.")
                    source_language = "Inglés"

            with st.expander("Previsualización del original", expanded=False):
                preview_text = original_content[:1500] + " [...]" if len(original_content) > 1500 else original_content
                st.text(preview_text)
        except Exception as e:
            st.error(f"Error al leer el archivo: {str(e)}")

        if st.button("Realizar Traducción Literaria", type="primary", use_container_width=True):
            try:
                translator = LiteraryTranslator(chunk_size=settings.CHUNK_SIZE)

                with st.spinner("Procesando documento..."):
                    original_content = FileHandler.read_file(uploaded_file)

                st.info(f"Usando modelo: **{model_choice}**, traduciendo de **{source_language}** a **{target_language}**")

                with st.status("Proceso de traducción literaria en curso...", expanded=True) as status:
                    translated_content = translator.translate(original_content, model_choice, source_language, target_language)
                    status.update(label="✓ Traducción completada con fidelidad literaria", state="complete")

                    with st.expander("Vista previa de la traducción", expanded=False):
                        st.text(translated_content[:2000] + " [...]")

                    file_bytes, output_name = FileHandler.create_output_file(
                        translated_content,
                        uploaded_file.name,
                        target_language
                    )

                    st.download_button(
                        label="Descargar Traducción Literaria",
                        data=file_bytes,
                        file_name=output_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary"
                    )

            except Exception as e:
                st.error(f"Error durante la traducción: {str(e)}")
                logger.error(f"Error en la interfaz de usuario: {e}")

if __name__ == "__main__":
    main_ui()
