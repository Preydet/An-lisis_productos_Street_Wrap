"""
Módulo de Configuración del Proyecto
Centraliza rutas y parámetros del análisis
"""
from pathlib import Path

# Ruta raíz del proyecto 
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpetas principales
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Crear carpetas automáticamente si no existen
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Rutas de archivos por defecto
DEFAULT_CSV_PATH = DATA_DIR / "cantidad_productos.csv"
OUTPUT_HTML_REPORT = BASE_DIR / "index.html"  # Guardado en la raíz para despliegue directo