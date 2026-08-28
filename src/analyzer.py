"""
Módulo para el análisis del conteo de ventas por producto
"""
import pandas as pd

class SalesAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = self._clean_data(df)

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza, unifica formato de texto y elimina prefijos de combos."""
        df_clean = df.copy()
        
        # 1. Asegurar formato string y eliminar espacios en extremos
        df_clean['Producto'] = df_clean['Producto'].astype(str).str.strip()
        
        # 2. Remover prefijos numerados de combos ("2.Pollo...", "2. Pollo...")
        df_clean['Producto'] = df_clean['Producto'].str.replace(r'^\d+\.\s*', '', regex=True)
        
        # 3. Unificar formato de texto (Title case para homogeneizar MAYÚSCULAS/minúsculas)
        df_clean['Producto'] = df_clean['Producto'].str.title()
        
        # 4. Limpiar espacios dobles o residuales
        df_clean['Producto'] = df_clean['Producto'].str.replace(r'\s+', ' ', regex=True).str.strip()
        
        # 5. Agrupar obligatoriamente por el nombre unificado del producto
        df_clean = (df_clean.groupby('Producto', as_index=False)['Cantidad_Vendida']
                    .sum()
                    .sort_values(by='Cantidad_Vendida', ascending=False))
        
        return df_clean

    def get_top_products(self, top_n: int = 1000) -> pd.DataFrame:
        """Obtiene el Top N de productos más vendidos consolidando registros."""
        return (self.df.groupby('Producto', as_index=False)['Cantidad_Vendida']
                .sum()
                .sort_values(by='Cantidad_Vendida', ascending=False)
                .head(top_n))

    def search_product(self, query: str) -> pd.DataFrame:
        """Consulta cuántas veces se vendió un producto según coincidencia de texto."""
        mask = self.df['Producto'].str.contains(query, case=False, na=False)
        return (self.df[mask]
                .groupby('Producto', as_index=False)['Cantidad_Vendida']
                .sum()
                .sort_values(by='Cantidad_Vendida', ascending=False))