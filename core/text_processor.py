import re
import textwrap

class TextProcessor:
    @staticmethod
    def preserve_literary_structure(original, translated):
        original_paragraphs = re.split(r'\n\s*\n', original)
        translated_paragraphs = re.split(r'\n\s*\n', translated)
        
        translated = translated.replace('[PAGE_BREAK]', '\n\n--- SALTO DE PÁGINA ---\n\n')
        
        if len(original_paragraphs) == len(translated_paragraphs):
            reconstructed = []
            for o_para, t_para in zip(original_paragraphs, translated_paragraphs):
                if o_para.endswith('\n'):
                    reconstructed.append(t_para + '\n')
                else:
                    reconstructed.append(t_para)
            return '\n\n'.join(reconstructed)
        
        return '\n\n'.join(translated_paragraphs)
    
    @staticmethod
    def split_preserving_context(text, chunk_size):
        chunks = []
        current_chunk = ""
        context_breakers = [
            "\n\n--- SALTO DE PÁGINA ---\n\n",
            "\n\nCHAPTER ",
            "\n\nSCENE ",
            "\n\nACT ",
            "\n\n• • •\n\n"
        ]
        
        for section in re.split(f"({'|'.join(context_breakers)})", text):
            if len(current_chunk) + len(section) <= chunk_size:
                current_chunk += section
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                
                if len(section) > chunk_size:
                    sub_sections = re.split(r'(\n\s*\n)', section)
                    sub_current = ""
                    for sub in sub_sections:
                        if len(sub_current) + len(sub) > chunk_size:
                            if sub_current:
                                chunks.append(sub_current)
                            sub_current = sub
                        else:
                            sub_current += sub
                    if sub_current:
                        chunks.append(sub_current)
                else:
                    current_chunk = section
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks