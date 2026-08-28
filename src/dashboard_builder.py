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

def acortar_texto(texto, idx, max_chars=35):
    """
    Acorta el texto e inyecta un espacio invisible de ancho cero (Zero-Width Space)
    basado en el índice para garantízar que cada etiqueta sea 100% única en el eje Y.
    """
    str_t = str(texto).strip()
    corta = str_t[:max_chars - 3] + '...' if len(str_t) > max_chars else str_t
    # \u200b es un carácter invisible que evita la colisión de nombres iguales en Plotly
    return corta + ('\u200b' * idx)

class DashboardBuilder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def _filter_and_group(self, df, categories=None):
        filtered = df.copy()
        
        if categories:
            mask = filtered['Producto'].apply(
                lambda p: any(c.lower() in str(p).lower() for c in categories)
            )
            filtered = filtered[mask]
        
        # Agrupar y ordenar estrictamente de MENOR a MAYOR
        grouped = (filtered.groupby('Producto', as_index=False)['Cantidad_Vendida']
                   .sum()
                   .sort_values(by='Cantidad_Vendida', ascending=True))
        
        return grouped

    def create_sales_chart(self):
        full_df = self.analyzer.get_top_products(top_n=1000)

        df_top20 = self._filter_and_group(full_df).tail(20)
        
        df_sin_extras_raw = full_df[~full_df['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)]
        df_sin_extras = self._filter_and_group(df_sin_extras_raw).tail(20)
        
        df_solo_extras_raw = full_df[full_df['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)]
        df_solo_extras = self._filter_and_group(df_solo_extras_raw).tail(20)
        
        df_base = self._filter_and_group(full_df, PRODUCTOS_BASE)
        df_granos = self._filter_and_group(full_df, PRODUCTOS_GRANOS_LEGUMBRES)
        df_verduras = self._filter_and_group(full_df, PRODUCTOS_VERDURAS)
        df_toppings = self._filter_and_group(full_df, PRODUCTOS_TOPPINGS)
        df_salsas = self._filter_and_group(full_df, PRODUCTOS_SALSAS)
        df_top50 = self._filter_and_group(full_df).tail(50)

        fig = go.Figure()

        traces = [
            (df_top20, 'Viridis'),
            (df_sin_extras, 'Plasma'),
            (df_solo_extras, 'Cividis'),
            (df_base, 'YlOrRd'),
            (df_granos, 'Greens'),
            (df_verduras, 'emrld'),
            (df_toppings, 'pubu'),
            (df_salsas, 'Reds'),
            (df_top50, 'Turbo')
        ]

        for i, (df, scale) in enumerate(traces):
            x_vals = df['Cantidad_Vendida'].tolist() if not df.empty else []
            y_raw = df['Producto'].tolist() if not df.empty else []
            
            # Generar etiquetas con caracteres invisibles únicos para evitar nombres duplicados
            y_unique_short = [acortar_texto(p, idx) for idx, p in enumerate(y_raw)]

            fig.add_trace(go.Bar(
                x=x_vals,
                y=y_unique_short,
                orientation='h',
                visible=(i == 0),
                customdata=y_raw,
                marker=dict(
                    color=x_vals if x_vals else None, 
                    colorscale=scale
                ),
                hovertemplate="<b>%{customdata}</b><br>Cantidad: %{x:,}<extra></extra>"
            ))

        fig.update_layout(
            title=dict(text="<b>Top 20 Productos Más Vendidos</b>", font=dict(size=18)),
            height=600,
            template='plotly_white',
            showlegend=False,
            xaxis=dict(title="Unidades Vendidas"),
            yaxis=dict(
                type='category',
                categoryorder='array',  # Mantiene de forma estricta el orden indexado de los arrays de Python
                automargin=True
            ),
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