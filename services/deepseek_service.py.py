import requests
from config.settings import settings
from config.prompts import TranslationPrompts
from utils.logger import logger

class DeepSeekService:
    ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
    
    @classmethod
    def translate(cls, text):
        headers = {"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"}
        full_prompt = f"{TranslationPrompts.DEEPSEEK_PROMPT}\n\nTEXTO A TRADUCIR:\n{text}"
        
        payload = {
            "model": "deepseek-r1",
            "messages": [{"role": "user", "content": full_prompt}],
            "max_tokens": 4000,
            "temperature": 0.1,
            "top_p": 0.95,
            "frequency_penalty": 0.2
        }
        
        try:
            response = requests.post(
                cls.ENDPOINT,
                headers=headers,
                json=payload,
                timeout=settings.TIMEOUT
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            logger.error(f"Error DeepSeek API: {str(e)}")
            raise