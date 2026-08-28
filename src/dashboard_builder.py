"""
Módulo para la construcción de gráficos interactivos con Plotly
"""
import plotly.graph_objects as go
from product_categories import PRODUCTOS_BASE

class DashboardBuilder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def create_sales_chart(self) -> go.Figure:
        """Crea la figura de Plotly con todas sus trazas listas para ser controladas por HTML/JS."""
        full_df = self.analyzer.get_top_products(top_n=1000)

        # Preparación de subconjuntos
        df_top20 = full_df.head(20).sort_values(by='Cantidad_Vendida', ascending=True)
        df_sin_extras = full_df[~full_df['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)].head(20).sort_values(by='Cantidad_Vendida', ascending=True)
        df_solo_extras = full_df[full_df['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)].head(20).sort_values(by='Cantidad_Vendida', ascending=True)
        
        df_base = full_df[
            full_df['Producto'].apply(
                lambda p: any(b.lower() in p.lower() for b in PRODUCTOS_BASE)
            )
        ].sort_values(by='Cantidad_Vendida', ascending=True)

        df_top50 = full_df.head(50).sort_values(by='Cantidad_Vendida', ascending=True)

        fig = go.Figure()

        # Traza 0: Top 20 General
        fig.add_trace(go.Bar(
            x=df_top20['Cantidad_Vendida'], y=df_top20['Producto'],
            orientation='h', visible=True,
            marker=dict(color=df_top20['Cantidad_Vendida'], colorscale='Viridis'),
            hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
        ))

        # Traza 1: Sin Extras
        fig.add_trace(go.Bar(
            x=df_sin_extras['Cantidad_Vendida'], y=df_sin_extras['Producto'],
            orientation='h', visible=False,
            marker=dict(color=df_sin_extras['Cantidad_Vendida'], colorscale='Plasma'),
            hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
        ))

        # Traza 2: Solo Extras
        fig.add_trace(go.Bar(
            x=df_solo_extras['Cantidad_Vendida'], y=df_solo_extras['Producto'],
            orientation='h', visible=False,
            marker=dict(color=df_solo_extras['Cantidad_Vendida'], colorscale='Cividis'),
            hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
        ))

        # Traza 3: Solo Base
        fig.add_trace(go.Bar(
            x=df_base['Cantidad_Vendida'], y=df_base['Producto'],
            orientation='h', visible=False,
            marker=dict(color=df_base['Cantidad_Vendida'], colorscale='YlOrRd'),
            hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
        ))

        # Traza 4: Top 50 General
        fig.add_trace(go.Bar(
            x=df_top50['Cantidad_Vendida'], y=df_top50['Producto'],
            orientation='h', visible=False,
            marker=dict(color=df_top50['Cantidad_Vendida'], colorscale='Turbo'),
            hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
        ))

        # Configuración limpia del layout (sin controles internos colisionando)
        fig.update_layout(
            title=dict(text="<b>Top 20 Productos Más Vendidos</b>", font=dict(size=18)),
            height=600,
            template='plotly_white',
            showlegend=False,
            xaxis=dict(title="Unidades Vendidas"),
            yaxis=dict(type='category', automargin=True),
            margin=dict(l=220, r=40, t=50, b=50)
        )

        return fig, len(df_base)