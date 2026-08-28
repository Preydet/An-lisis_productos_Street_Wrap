"""
Módulo para el análisis del conteo de ventas por producto
"""
import pandas as pd

class SalesAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_top_products(self, top_n: int = 20) -> pd.DataFrame:
        """Obtiene el Top N de productos más vendidos por cantidad."""
        return (self.df.groupby(['ID', 'Producto'])['Cantidad_Vendida']
                .sum()
                .reset_index()
                .sort_values(by='Cantidad_Vendida', ascending=False)
                .head(top_n))

    def search_product(self, query: str) -> pd.DataFrame:
        """Consulta cuántas veces se vendió un producto según coincidencia de texto."""
        mask = self.df['Producto'].str.contains(query, case=False, na=False)
        return (self.df[mask]
                .groupby(['ID', 'Producto'])['Cantidad_Vendida']
                .sum()
                .reset_index()
                .sort_values(by='Cantidad_Vendida', ascending=False))