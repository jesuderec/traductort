import sys
import os

# Agrega la ruta raíz del proyecto al sys.path para manejar las importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui import streamlit_ui

if __name__ == "__main__":
    streamlit_ui.main_ui()
