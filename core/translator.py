from services.deepseek_service import DeepSeekService
from services.openai_service import OpenAIService
from services.gemini_service import GeminiService
from core.text_processor import TextProcessor
from config.prompts import TranslationPrompts
import logging

logger = logging.getLogger(__name__)

class LiteraryTranslator:
    def __init__(self, chunk_size=2000):
        self.chunk_size = chunk_size

    def translate(self, content, model_choice, source_language, target_language):
        logger.info(f"Iniciando traducción con el modelo: {model_choice} de {source_language} a {target_language}")
        cleaned_content = TextProcessor.clean_text(content)

        if model_choice == "DeepSeek-R1 (Literario)":
            return self._translate_chunks(cleaned_content, self._translate_deepseek, source_language, target_language)
        elif model_choice == "GPT-4-Turbo (Literatura Fina)":
            return self._translate_chunks(cleaned_content, self._translate_openai, source_language, target_language)
        elif model_choice == "Gemini 1.5 Pro (Literario)":
            return self._translate_chunks(cleaned_content, self._translate_gemini, source_language, target_language)
        else:
            return self._hybrid_translation(cleaned_content, source_language, target_language)

    def _translate_chunks(self, content, translate_func, source_language, target_language):
        chunks = TextProcessor.split_preserving_context(content, self.chunk_size)
        logger.info(f"Texto dividido en {len(chunks)} fragmentos.")
        translated_chunks = []

        for i, chunk in enumerate(chunks):
            logger.info(f"Traduciendo fragmento {i+1}/{len(chunks)}...")
            translated = translate_func(chunk, source_language, target_language)
            reconstructed = TextProcessor.preserve_literary_structure(chunk, translated)
            translated_chunks.append(reconstructed)
            logger.info(f"Fragmento {i+1} traducido exitosamente.")

        logger.info("Todos los fragmentos traducidos. Uniendo...")
        return ''.join(translated_chunks)

    def _translate_deepseek(self, chunk, source_language, target_language):
        return DeepSeekService.translate(chunk, source_language, target_language)

    def _translate_openai(self, chunk, source_language, target_language):
        return OpenAIService.translate(chunk, source_language, target_language)

    def _translate_gemini(self, chunk, source_language, target_language):
        return GeminiService.translate(chunk, source_language, target_language)

    def _hybrid_translation(self, content, source_language, target_language):
        chunks = TextProcessor.split_preserving_context(content, self.chunk_size)
        logger.info(f"Texto dividido para traducción híbrida en {len(chunks)} fragmentos.")
        translated_chunks = []

        for i, chunk in enumerate(chunks):
            logger.info(f"Iniciando traducción base (DeepSeek) para el fragmento {i+1}/{len(chunks)}...")
            base_translation = DeepSeekService.translate(chunk, source_language, target_language)
            logger.info(f"Traducción base completada. Iniciando refinamiento (OpenAI) para el fragmento {i+1}/{len(chunks)}...")
            refined_translation = OpenAIService.translate(
                base_translation,
                prompt=TranslationPrompts.HYBRID_REVISION_PROMPT.format(target_language=target_language)
            )
            reconstructed = TextProcessor.preserve_literary_structure(chunk, refined_translation)
            translated_chunks.append(reconstructed)
            logger.info(f"Fragmento {i+1} refinado y traducido exitosamente.")

        logger.info("Todos los fragmentos híbridos traducidos. Uniendo...")
        return ''.join(translated_chunks)
