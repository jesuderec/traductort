import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Configuración de traducción
    CHUNK_SIZE = 2500  # Tamaño de segmentos para preservar contexto
    TIMEOUT = 180      # Tiempo máximo de espera para APIs
    
    # Modelos disponibles
    MODELS = {
        "DeepSeek-R1 (Literario)": "deepseek",
        "GPT-4-Turbo (Literatura Fina)": "openai",
        "Mixto (DeepSeek + GPT-4 Revisión)": "hybrid"
    }
    
    @classmethod
    def validate_keys(cls):
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY no configurada")
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no configurada")

settings = Settings()