import os
import logging
from pathlib import Path

# Intenta cargar dotenv pero no falla si no está instalado
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logging.warning("python-dotenv no instalado. Usando variables de entorno del sistema")

# Cargar variables
def load_config():
    # 1. Intento: Variables de entorno del sistema
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    # 2. Intento: Archivo .env (solo en desarrollo)
    if not (deepseek_key and openai_key) and DOTENV_AVAILABLE:
        try:
            env_path = Path(__file__).resolve().parent.parent / ".env"
            load_dotenv(dotenv_path=env_path)
            deepseek_key = os.getenv("DEEPSEEK_API_KEY")
            openai_key = os.getenv("OPENAI_API_KEY")
        except Exception as e:
            logging.error(f"Error cargando .env: {e}")
    
    # 3. Intento: Secrets de Streamlit (para producción)
    if not (deepseek_key and openai_key):
        try:
            import streamlit as st
            deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")
            openai_key = st.secrets.get("OPENAI_API_KEY")
        except:
            pass
    
    return {
        "DEEPSEEK_API_KEY": deepseek_key,
        "OPENAI_API_KEY": openai_key,
        "DEEPSEEK_MODEL": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    }

settings = load_config()

# Validación final
if not settings["DEEPSEEK_API_KEY"]:
    logging.error("Falta DEEPSEEK_API_KEY")
if not settings["OPENAI_API_KEY"]:
    logging.error("Falta OPENAI_API_KEY")
