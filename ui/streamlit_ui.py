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
                value=False,  # <-- Cambiado a False
                help="Mantener epígrafes, notas al pie, formatos especiales"
            )
            cultural_notes = st.checkbox(
                "Añadir notas culturales", 
                value=False,  # <-- Cambiado a False
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
