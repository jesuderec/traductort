import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Obtener ruta base
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno
try:
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        logger.warning(".env file not found. Using system environment variables.")
except Exception as e:
    logger.error(f"Error loading .env file: {e}")

class Settings:
    # DeepSeek
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")  # Valor por defecto
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    
    # Validar configuraciones
    @classmethod
    def validate(cls):
        missing = []
        if not cls.DEEPSEEK_API_KEY:
            missing.append("DEEPSEEK_API_KEY")
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        
        if missing:
            logger.error(f"Missing environment variables: {', '.join(missing)}")
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# Validar al importar
Settings.validate()

settings = Settings()
