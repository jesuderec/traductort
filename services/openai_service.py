import logging
from openai import OpenAI
from config.settings import settings
from config.prompts import TranslationPrompts

logger = logging.getLogger(__name__)

class OpenAIService:
    @classmethod
    def translate(cls, text, target_language, prompt=None, model=None):
        logger.info(f"Iniciando llamada a la API de OpenAI para traducir a {target_language}.")
        if not prompt:
            prompt = TranslationPrompts.OPENAI_PROMPT.format(target_language=target_language)
        
        if not model:
            model = settings.OPENAI_MODEL
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY, timeout=settings.TIMEOUT)
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            logger.info("Llamada a la API de OpenAI exitosa.")
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error en la API de OpenAI: {str(e)}")
            raise
