import logging
from config.settings import settings
from utils.api_utils import ask_deepseek, ask_openai

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    print("Configuración cargada:")
    print(f"Modelo DeepSeek: {settings.DEEPSEEK_MODEL}")
    print(f"Modelo OpenAI: {settings.OPENAI_MODEL}")
    
    prompt = "Explica la teoría de la relatividad en 3 líneas"
    
    print("\nConsultando DeepSeek...")
    deepseek_response = ask_deepseek(prompt)
    print(f"Respuesta DeepSeek:\n{deepseek_response}")
    
    print("\nConsultando OpenAI...")
    openai_response = ask_openai(prompt)
    print(f"Respuesta OpenAI:\n{openai_response}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("Error fatal en la aplicación")
        print(f"Error crítico: {e}. Por favor revisa los logs.")
