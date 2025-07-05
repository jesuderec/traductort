from config.settings import settings
from ui.streamlit_ui import main_ui
import os

if __name__ == "__main__":
    try:
        settings.validate_keys()
        main_ui()
    except ValueError as e:
        import streamlit as st
        st.error(f"Error de configuración: {str(e)}")
        st.info("Por favor, configura las variables de entorno DEEPSEEK_API_KEY y OPENAI_API_KEY")
    except Exception as e:
        import streamlit as st
        st.error(f"Error inesperado: {str(e)}")