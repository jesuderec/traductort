import logging
from openai import OpenAI
from config.settings import settings
from config.prompts import TranslationPrompts

logger = logging.getLogger(__name__)

class DeepSeekService:
    @classmethod
    def translate(cls, text, target_language):
        logger.info(f"Iniciando llamada a la API de DeepSeek para traducir a {target_language}.")
        client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1",
            timeout=settings.TIMEOUT
        )
        
        full_prompt = f"{TranslationPrompts.DEEPSEEK_PROMPT.format(target_language=target_language)}\n\nTEXTO A TRADUCIR:\n{text}"
        
        try:
            response = client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.1,
                max_tokens=4000
            )
            logger.info("Llamada a la API de DeepSeek exitosa.")
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error en la API de DeepSeek: {str(e)}")
            raise
