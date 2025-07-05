import openai
from config.settings import settings
from config.prompts import TranslationPrompts
from utils.logger import logger

class OpenAIService:
    @classmethod
    def translate(cls, text, model="gpt-4-turbo", prompt=None):
        if not prompt:
            prompt = TranslationPrompts.OPENAI_PROMPT
        
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=4000,
                top_p=0.9,
                presence_penalty=0.1,
                frequency_penalty=0.2
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error OpenAI API: {str(e)}")
            raise