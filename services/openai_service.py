from openai import OpenAI
from config.settings import settings
from config.prompts import TranslationPrompts
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    @classmethod
    def translate(cls, text, prompt=None, model=None):
        if not prompt:
            prompt = TranslationPrompts.OPENAI_PROMPT
        
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
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error OpenAI API: {str(e)}")
            raise
