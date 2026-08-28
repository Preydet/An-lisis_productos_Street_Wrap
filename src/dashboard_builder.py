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

TOTAL_ORDENES = 11617

def acortar_texto(texto, idx, max_chars=35):
    str_t = str(texto).strip()
    corta = str_t[:max_chars - 3] + '...' if len(str_t) > max_chars else str_t
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
            
            # Calcular porcentaje sobre 11,617 órdenes
            pct_vals = [(cant / TOTAL_ORDENES) * 100 for cant in x_vals]
            text_labels = [f" {cant:,} ({pct:.1f}%)" if cant > 0 else "" for cant, pct in zip(x_vals, pct_vals)]
            
            y_unique_short = [acortar_texto(p, idx) for idx, p in enumerate(y_raw)]

            fig.add_trace(go.Bar(
                x=x_vals,
                y=y_unique_short,
                orientation='h',
                visible=(i == 0),
                text=text_labels,
                textposition='outside',
                cliponaxis=False,  # Permite que las etiquetas se muestren aunque la barra sea muy corta
                customdata=list(zip(y_raw, pct_vals)),
                marker=dict(
                    color=x_vals if x_vals else None, 
                    colorscale=scale
                ),
                hovertemplate="<b>%{customdata[0]}</b><br>Cantidad: %{x:,} unidades<br>Presencia en Órdenes: <b>%{customdata[1]:.1f}%</b><extra></extra>"
            ))

        fig.update_layout(
            title=dict(text="<b>Top 20 Productos Más Vendidos</b>", font=dict(size=18)),
            height=600,
            template='plotly_white',
            showlegend=False,
            xaxis=dict(title="Unidades Vendidas"),
            yaxis=dict(
                type='category',
                categoryorder='array',
                automargin=True
            ),
            margin=dict(l=220, r=120, t=50, b=50) # Margen derecho ampliado a 120px para dar espacio al texto
        )

        counts = {
            'total_ordenes': TOTAL_ORDENES,
            'base': len(df_base),
            'granos': len(df_granos),
            'verduras': len(df_verduras),
            'toppings': len(df_toppings),
            'salsas': len(df_salsas)
        }

        return fig, counts