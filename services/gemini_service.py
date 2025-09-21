import google.generativeai as genai
from config.settings import settings
from config.prompts import TranslationPrompts
import logging

logger = logging.getLogger(__name__)
genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiService:
    @classmethod
    def translate(cls, text, source_language, target_language):
        logger.info(f"Iniciando llamada a la API de Gemini para traducir de {source_language} a {target_language}.")
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            full_prompt = f"{TranslationPrompts.DEEPSEEK_PROMPT.format(source_language=source_language, target_language=target_language)}\n\nTEXTO A TRADUCIR:\n{text}"

            response = model.generate_content(full_prompt)

            return response.text.strip()
        except Exception as e:
            logger.error(f"Error Gemini API: {str(e)}")
            raise
