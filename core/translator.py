from services.deepseek_service import DeepSeekService
from services.openai_service import OpenAIService
from core.text_processor import TextProcessor
from config.settings import settings
from config.prompts import TranslationPrompts

class LiteraryTranslator:
    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
    
    def translate(self, content, model_choice):
        if model_choice == "DeepSeek-R1 (Literario)":
            return self._translate_chunks(content, self._translate_deepseek)
        elif model_choice == "GPT-4-Turbo (Literatura Fina)":
            return self._translate_chunks(content, self._translate_openai)
        else:
            return self._hybrid_translation(content)
    
    def _translate_chunks(self, content, translate_func):
        chunks = TextProcessor.split_preserving_context(content, self.chunk_size)
        translated_chunks = []
        
        for chunk in chunks:
            translated = translate_func(chunk)
            reconstructed = TextProcessor.preserve_literary_structure(chunk, translated)
            translated_chunks.append(reconstructed)
        
        return ''.join(translated_chunks)
    
    def _translate_deepseek(self, chunk):
        return DeepSeekService.translate(chunk)
    
    def _translate_openai(self, chunk):
        return OpenAIService.translate(chunk)
    
    def _hybrid_translation(self, content):
        chunks = TextProcessor.split_preserving_context(content, self.chunk_size)
        translated_chunks = []
        
        for chunk in chunks:
            base_translation = DeepSeekService.translate(chunk)
            refined_translation = OpenAIService.translate(
                base_translation,
                prompt=TranslationPrompts.HYBRID_REVISION_PROMPT
            )
            reconstructed = TextProcessor.preserve_literary_structure(chunk, refined_translation)
            translated_chunks.append(reconstructed)
        
        return ''.join(translated_chunks)