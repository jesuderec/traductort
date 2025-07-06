import re

class TextProcessor:
    @staticmethod
    def preserve_literary_structure(original, translated):
        original_paragraphs = re.split(r'\n\s*\n', original)
        translated_paragraphs = re.split(r'\n\s*\n', translated)
        
        # Conservar saltos de página especiales
        translated = translated.replace('[PAGE_BREAK]', '\n\n--- SALTO DE PÁGINA ---\n\n')
        
        if len(original_paragraphs) == len(translated_paragraphs):
            reconstructed = []
            for o_para, t_para in zip(original_paragraphs, translated_paragraphs):
                # Conservar saltos de línea al final del párrafo original
                if o_para.endswith('\n'):
                    reconstructed.append(t_para + '\n')
                else:
                    reconstructed.append(t_para)
            return '\n\n'.join(reconstructed)
        
        return '\n\n'.join(translated_paragraphs)
    
    @staticmethod
    def split_preserving_context(text, chunk_size):
        if len(text) <= chunk_size:
            return [text]
        
        # Dividir por párrafos primero
        paragraphs = re.split(r'(\n\s*\n)', text)
        chunks = []
        current_chunk = ""
        
        for i, part in enumerate(paragraphs):
            if len(current_chunk) + len(part) <= chunk_size:
                current_chunk += part
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = part
                
                # Si la parte actual es muy grande, dividir en oraciones
                if len(current_chunk) > chunk_size:
                    sentences = re.split(r'(?<=[.!?])\s+', current_chunk)
                    current_chunk = ""
                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) <= chunk_size:
                            current_chunk += sentence + " "
                        else:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                            current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
