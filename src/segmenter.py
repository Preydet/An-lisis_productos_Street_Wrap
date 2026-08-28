"""
Módulo para segmentación y filtrado personalizado de productos
"""
import pandas as pd
from typing import List

class ProductSegmenter:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def filter_by_products(self, product_names: List[str]) -> pd.DataFrame:
        """Filtra la tabla para incluir solo una lista exacta de productos."""
        return self.df[self.df['Producto'].isin(product_names)].copy()

    def filter_by_keywords(self, keywords: List[str], exclude_extras: bool = False) -> pd.DataFrame:
        """
        Filtra productos que contengan cualquiera de las palabras clave.
        Permite opcionalmente excluir ingredientes/extras (*Extra).
        """
        pattern = '|'.join(keywords)
        mask = self.df['Producto'].str.contains(pattern, case=False, na=False)
        
        df_filtered = self.df[mask].copy()

        if exclude_extras:
            df_filtered = df_filtered[~df_filtered['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)]

        return df_filtered

    def exclude_extras(self) -> pd.DataFrame:
        """Remueve todos los ítems marcados como (*Extra) para ver solo platillos/productos finales."""
        return self.df[~self.df['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)].copy()