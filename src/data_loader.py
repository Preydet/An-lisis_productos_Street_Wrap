"""
Módulo para la carga y limpieza de datos enfocada en Cantidades Vendidas
"""
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoader:
    def __init__(self, file_path: str | Path):
        self.file_path = file_path

    def load_raw_data(self) -> pd.DataFrame:
        """Carga el CSV interpretando la columna Cantidad como texto."""
        logging.info(f"Cargando archivo desde: {self.file_path}")
        return pd.read_csv(self.file_path, dtype={'Cantidad': str})

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Procesa y limpia la columna de cantidades vendidas."""
        df_clean = df[['ID', 'Producto', 'Cantidad']].copy()

        def parse_cantidad(val):
            if pd.isna(val):
                return 0.0
            val_clean = str(val).strip().replace('.', '')
            try:
                return float(val_clean)
            except ValueError:
                return 0.0

        df_clean['Cantidad_Vendida'] = df_clean['Cantidad'].apply(parse_cantidad)
        logging.info("Limpieza de datos completada exitosamente.")
        return df_clean[['ID', 'Producto', 'Cantidad_Vendida']]