"""
Módulo para la construcción de gráficos interactivos con Plotly
"""
import plotly.graph_objects as go
from product_categories import (
    PRODUCTOS_BASE,
    PRODUCTOS_GRANOS_LEGUMBRES,
    PRODUCTOS_VERDURAS,
    PRODUCTOS_TOPPINGS,
    PRODUCTOS_SALSAS
)

class DashboardBuilder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def _filter_df_by_list(self, df, categories):
        """Filtra el dataframe buscando coincidencias parciales con la lista de categorías."""
        filtered = df[
            df['Producto'].apply(
                lambda p: any(c.lower() in str(p).lower() for c in categories)
            )
        ].sort_values(by='Cantidad_Vendida', ascending=True)
        return filtered

    def create_sales_chart(self):
        full_df = self.analyzer.get_top_products(top_n=1000)

        # Generar dataframes por categoría
        df_top20 = full_df.head(20).sort_values(by='Cantidad_Vendida', ascending=True)
        df_sin_extras = full_df[~full_df['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)].head(20).sort_values(by='Cantidad_Vendida', ascending=True)
        df_solo_extras = full_df[full_df['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)].head(20).sort_values(by='Cantidad_Vendida', ascending=True)
        
        df_base = self._filter_df_by_list(full_df, PRODUCTOS_BASE)
        df_granos = self._filter_df_by_list(full_df, PRODUCTOS_GRANOS_LEGUMBRES)
        df_verduras = self._filter_df_by_list(full_df, PRODUCTOS_VERDURAS)
        df_toppings = self._filter_df_by_list(full_df, PRODUCTOS_TOPPINGS)
        df_salsas = self._filter_df_by_list(full_df, PRODUCTOS_SALSAS)
        df_top50 = full_df.head(50).sort_values(by='Cantidad_Vendida', ascending=True)

        fig = go.Figure()

        # Lista de configuraciones con escalas de colores válidas
        traces = [
            (df_top20, 'Viridis'),        # Index 0: Top 20
            (df_sin_extras, 'Plasma'),    # Index 1: Sin Extras
            (df_solo_extras, 'Cividis'),  # Index 2: Solo Extras
            (df_base, 'YlOrRd'),          # Index 3: Base
            (df_granos, 'Greens'),        # Index 4: Granos/Legumbres
            (df_verduras, 'emrld'),       # Index 5: Verduras (corregido de Emerald a emrld)
            (df_toppings, 'pubu'),        # Index 6: Toppings
            (df_salsas, 'Reds'),          # Index 7: Salsas
            (df_top50, 'Turbo')           # Index 8: Top 50
        ]

        for i, (df, scale) in enumerate(traces):
            x_vals = df['Cantidad_Vendida'].tolist() if not df.empty else []
            y_vals = df['Producto'].tolist() if not df.empty else []

            fig.add_trace(go.Bar(
                x=x_vals,
                y=y_vals,
                orientation='h',
                visible=(i == 0),
                marker=dict(
                    color=x_vals if x_vals else None, 
                    colorscale=scale
                ),
                hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
            ))

        fig.update_layout(
            title=dict(text="<b>Top 20 Productos Más Vendidos</b>", font=dict(size=18)),
            height=600,
            template='plotly_white',
            showlegend=False,
            xaxis=dict(title="Unidades Vendidas"),
            yaxis=dict(type='category', automargin=True),
            margin=dict(l=220, r=40, t=50, b=50)
        )

        counts = {
            'base': len(df_base),
            'granos': len(df_granos),
            'verduras': len(df_verduras),
            'toppings': len(df_toppings),
            'salsas': len(df_salsas)
        }

        return fig, counts