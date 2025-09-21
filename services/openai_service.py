from openai import OpenAI
from config.settings import settings
from config.prompts import TranslationPrompts
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    @classmethod
    def translate(cls, text, source_language, target_language, prompt=None, model=None):
        logger.info(f"Iniciando llamada a la API de OpenAI para traducir de {source_language} a {target_language}.")
        if not prompt:
            prompt = TranslationPrompts.OPENAI_PROMPT.format(source_language=source_language, target_language=target_language)

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
