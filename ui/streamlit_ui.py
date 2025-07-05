import streamlit as st
from config.settings import settings
from core.file_handler import FileHandler
from core.translator import LiteraryTranslator

def setup_streamlit():
    st.set_page_config(
        page_title="Traductor Literario Profesional",
        page_icon="📖",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    <style>
        /* Estilos personalizados */
    </style>
    """, unsafe_allow_html=True)
    
    st.title("✒️ Traductor Literario Profesional")
    st.markdown("""
    <div style="text-align: center; border-bottom: 1px solid #d4c9b1; padding-bottom: 20px; margin-bottom: 30px;">
        <i>Traducciones que respetan la voz del autor, recursos estilísticos y esencia literaria</i>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuración de Traducción")
        model_choice = st.selectbox(
            "Selecciona el modelo de traducción:",
            list(settings.MODELS.keys()),
            index=0,
            help="DeepSeek para prosa general, GPT-4 para poesía y textos complejos, Mixto para máxima fidelidad"
        )
        
        st.markdown("---")
        st.subheader("Opciones Avanzadas")
        preserve_special = st.checkbox(
            "Conservar elementos especiales", 
            value=True,
            help="Mantener epígrafes, notas al pie, formatos especiales"
        )
        cultural_notes = st.checkbox(
            "Añadir notas culturales", 
            value=True,
            help="Incluir explicaciones entre [ ] para referencias culturales"
        )
        
        st.markdown("---")
        st.info("""
        **Instrucciones:**
        1. Sube tu documento (PDF, DOCX, TXT)
        2. Selecciona modelo de traducción
        3. Inicia la traducción
        4. Descarga el resultado conservando el estilo literario
        """)
        
        return model_choice, preserve_special, cultural_notes

def main_ui():
    setup_streamlit()
    model_choice, preserve_special, cultural_notes = render_sidebar()
    
    uploaded_file = st.file_uploader(
        "Sube tu obra literaria",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False
    )
    
    if uploaded_file:
        with st.expander("Previsualización del original", expanded=False):
            try:
                original_content = FileHandler.read_file(uploaded_file)
                preview_text = original_content[:1500] + " [...]" if len(original_content) > 1500 else original_content
                st.text(preview_text)
            except Exception as e:
                st.error(f"Error al leer el archivo: {str(e)}")
        
        if st.button("Realizar Traducción Literaria", type="primary", use_container_width=True):
            try:
                translator = LiteraryTranslator()
                
                with st.spinner("Procesando documento..."):
                    original_content = FileHandler.read_file(uploaded_file)
                
                st.info(f"Usando modelo: **{model_choice}**")
                
                with st.status("Proceso de traducción literaria en curso...", expanded=True) as status:
                    translated_content = translator.translate(original_content, model_choice)
                    status.update(label="✓ Traducción completada con fidelidad literaria", state="complete")
                    
                    with st.expander("Vista previa de la traducción", expanded=False):
                        st.text(translated_content[:2000] + " [...]")
                    
                    file_bytes, output_name = FileHandler.create_output_file(
                        translated_content,
                        uploaded_file.name
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