from openai import OpenAI, APIConnectionError, APIError, RateLimitError
from config.settings import settings
import logging

# Configurar logging
logger = logging.getLogger(__name__)

def get_deepseek_client():
    """Crea y retorna cliente DeepSeek"""
    return OpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com/v1"
    )

def get_openai_client():
    """Crea y retorna cliente OpenAI"""
    return OpenAI(api_key=settings.OPENAI_API_KEY)

def ask_deepseek(prompt: str, model: str = None) -> str:
    """Envía un prompt a DeepSeek API"""
    client = get_deepseek_client()
    model = model or settings.DEEPSEEK_MODEL
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    except APIConnectionError as e:
        logger.error(f"Connection error: {e}")
        return "Error de conexión con DeepSeek"
    except RateLimitError as e:
        logger.error(f"Rate limit exceeded: {e}")
        return "Límite de solicitudes excedido"
    except APIError as e:
        logger.error(f"API error: {e}")
        return "Error en la API de DeepSeek"
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return "Error inesperado con DeepSeek"

def ask_openai(prompt: str, model: str = None) -> str:
    """Envía un prompt a OpenAI API"""
    client = get_openai_client()
    model = model or settings.OPENAI_MODEL
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    except APIConnectionError as e:
        logger.error(f"Connection error: {e}")
        return "Error de conexión con OpenAI"
    except RateLimitError as e:
        logger.error(f"Rate limit exceeded: {e}")
        return "Límite de solicitudes excedido"
    except APIError as e:
        logger.error(f"API error: {e}")
        return "Error en la API de OpenAI"
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return "Error inesperado con OpenAI"
