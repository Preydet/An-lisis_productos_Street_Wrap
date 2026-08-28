"""
Módulo para generación de reporte dinámico con filtros por categorías
"""
import plotly.graph_objects as go
import pandas as pd

class InteractiveReporter:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def build_dashboard_html(self, output_path: str):
        """Genera un reporte HTML limpio y legible con segmentador dinámico."""
        full_df = self.analyzer.get_top_products(top_n=1000)

        # 1. Definir los subsets de datos
        df_top20 = full_df.head(20).sort_values(by='Cantidad_Vendida', ascending=True)
        
        df_sin_extras = full_df[~full_df['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)].head(20).sort_values(by='Cantidad_Vendida', ascending=True)
        
        df_solo_extras = full_df[full_df['Producto'].str.contains(r'\(\*Extra\)', case=False, na=False)].head(20).sort_values(by='Cantidad_Vendida', ascending=True)
        
        df_top50 = full_df.head(50).sort_values(by='Cantidad_Vendida', ascending=True)

        fig = go.Figure()

        # Traza 0: Top 20 General
        fig.add_trace(go.Bar(
            x=df_top20['Cantidad_Vendida'],
            y=df_top20['Producto'],
            orientation='h',
            visible=True,
            marker=dict(color=df_top20['Cantidad_Vendida'], colorscale='Viridis'),
            hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
        ))

        # Traza 1: Sin Extras
        fig.add_trace(go.Bar(
            x=df_sin_extras['Cantidad_Vendida'],
            y=df_sin_extras['Producto'],
            orientation='h',
            visible=False,
            marker=dict(color=df_sin_extras['Cantidad_Vendida'], colorscale='Plasma'),
            hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
        ))

        # Traza 2: Solo Extras
        fig.add_trace(go.Bar(
            x=df_solo_extras['Cantidad_Vendida'],
            y=df_solo_extras['Producto'],
            orientation='h',
            visible=False,
            marker=dict(color=df_solo_extras['Cantidad_Vendida'], colorscale='Cividis'),
            hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
        ))

        # Traza 3: Top 50
        fig.add_trace(go.Bar(
            x=df_top50['Cantidad_Vendida'],
            y=df_top50['Producto'],
            orientation='h',
            visible=False,
            marker=dict(color=df_top50['Cantidad_Vendida'], colorscale='Turbo'),
            hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>"
        ))

        # Configurar menú desplegable
        buttons = [
            dict(
                label="📊 Top 20 Productos Más Vendidos",
                method="update",
                args=[{"visible": [True, False, False, False]},
                      {"title": "<b>Top 20 Productos Más Vendidos</b>", "height": 600}]
            ),
            dict(
                label="🥗 Solo Platos Principales (Sin *Extra)",
                method="update",
                args=[{"visible": [False, True, False, False]},
                      {"title": "<b>Top 20 Platos Principales (Excluye *Extra)</b>", "height": 600}]
            ),
            dict(
                label="🧀 Solo Ingredientes y Acompañamientos (*Extra)",
                method="update",
                args=[{"visible": [False, False, True, False]},
                      {"title": "<b>Top 20 Ingredientes e Extras Most Vendidos</b>", "height": 600}]
            ),
            dict(
                label="📋 Top 50 General",
                method="update",
                args=[{"visible": [False, False, False, True]},
                      {"title": "<b>Top 50 Productos Más Vendidos</b>", "height": 1100}]
            )
        ]

        fig.update_layout(
            title="<b>Top 20 Productos Más Vendidos</b>",
            height=600,
            template='plotly_white',
            showlegend=False,
            xaxis=dict(title="Unidades Vendidas"),
            yaxis=dict(type='category', automargin=True),
            updatemenus=[dict(
                active=0,
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )],
            margin=dict(l=200, r=40, t=100, b=50)
        )

        html_chart = fig.to_html(full_html=False, include_plotlyjs='cdn')

        html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Interactivo de Ventas</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8f9fa; padding: 20px; color: #333; }}
        .container {{ max-width: 1100px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }}
        h1 {{ color: #1e3c72; text-align: center; margin-bottom: 25px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📦 Reporte Interactivo de Ventas</h1>
        <div>{html_chart}</div>
    </div>
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)