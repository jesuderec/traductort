import os
import logging
from pathlib import Path

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings:
    def __init__(self):
        # Cargar variables de entorno
        self.DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        self.DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # Configuración adicional
        self.CHUNK_SIZE = 2000  # Tamaño de fragmentos
        self.TIMEOUT = 30       # Timeout para API
        self.MODELS = {         # Modelos para UI
            "DeepSeek-R1 (Literario)": "DeepSeek-R1 (Literario)",
            "GPT-4-Turbo (Literatura Fina)": "GPT-4-Turbo (Literatura Fina)",
            "Mixto (DeepSeek + GPT-4)": "Mixto (DeepSeek + GPT-4)"
        }
        
        # Validación
        self.validate()
    
    def validate(self):
        errors = []
        if not self.DEEPSEEK_API_KEY:
            errors.append("DEEPSEEK_API_KEY no configurada")
        if not self.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY no configurada")
        
        if errors:
            error_msg = "Error de configuración: " + ", ".join(errors)
            logger.error(error_msg)
            raise EnvironmentError(error_msg)
    
    def __str__(self):
        return (f"Settings: "
                f"DeepSeek({self.DEEPSEEK_MODEL}), "
                f"OpenAI({self.OPENAI_MODEL})")

# Crear instancia única
try:
    settings = Settings()
    logger.info("Configuración cargada exitosamente")
    logger.info(str(settings))
except EnvironmentError as e:
    logger.critical(str(e))
    # Para permitir que la aplicación continúe en modo de solo lectura
    settings = None
    raise
