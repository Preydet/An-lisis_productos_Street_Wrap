"""
Módulo para generación de gráfico dinámico de cantidades vendidas
"""
import plotly.express as px
import pandas as pd

class InteractiveReporter:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def build_dashboard_html(self, output_path: str, top_n: int = 20):
        """Genera un reporte HTML autónomo con un gráfico de barras interactivo."""
        top_df = self.analyzer.get_top_products(top_n)

        # Crear gráfico horizontal interactivo
        fig = px.bar(
            top_df.sort_values(by='Cantidad_Vendida', ascending=True),
            x='Cantidad_Vendida',
            y='Producto',
            orientation='h',
            title=f'<b>Top {top_n} Productos Más Vendidos (Unidades)</b>',
            labels={'Cantidad_Vendida': 'Unidades Vendidas', 'Producto': 'Producto'},
            template='plotly_white',
            color='Cantidad_Vendida',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=600, margin=dict(l=20, r=20, t=50, b=30))

        # Convertir gráfico a fragmento HTML autónomo
        html_chart = fig.to_html(full_html=False, include_plotlyjs='cdn')

        # Plantilla CSS/HTML para el reporte
        html_template = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte de Cantidad Vendida por Producto</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8f9fa; padding: 20px; color: #333; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }}
                h1 {{ color: #1e3c72; text-align: center; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📦 Reporte de Veces / Cantidad Vendida por Producto</h1>
                <div>{html_chart}</div>
            </div>
        </body>
        </html>
        """

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)