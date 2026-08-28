"""
Módulo para generación y exportación del reporte HTML final
"""
from src.dashboard_builder import DashboardBuilder

class InteractiveReporter:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.builder = DashboardBuilder(analyzer)

    def build_dashboard_html(self, output_path: str):
        fig, _ = self.builder.create_sales_chart()
        
        # Configuración de Plotly para activar responsividad nativa
        plotly_config = {
            'responsive': True,
            'displayModeBar': False  # Opcional: oculta la barra de herramientas molesta en móviles
        }

        div_chart = fig.to_html(
            full_html=False, 
            include_plotlyjs=False, 
            div_id="sales_plotly_div",
            config=plotly_config
        )

        html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Reporte Interactivo de Ventas 2026</title>
    <link rel="stylesheet" href="assets/css/styles.css">
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js" charset="utf-8"></script>
</head>
<body>
    <div class="container">
        <h1>📦 Reporte Interactivo de Ventas 2026</h1>
        
        <div class="filter-container">
            <span class="filter-label">🔍 Seleccionar Categoría / Vista:</span>
            <select id="categorySelector" class="filter-select" onchange="switchView(this.value)">
                <option value="0">📊 Top 20 General</option>
                <option value="1">🥗 Solo Platos Principales (Sin *Extra)</option>
                <option value="2">🧀 Solo Ingredientes y Acompañamientos (*Extra)</option>
                <option value="3">🥩 Categoría: Base / Proteínas</option>
                <option value="4">🌱 Categoría: Granos / Legumbres</option>
                <option value="5">🥦 Categoría: Verduras</option>
                <option value="6">🌰 Categoría: Toppings</option>
                <option value="7">🥫 Categoría: Salsas</option>
                <option value="8">📋 Top 50 General</option>
            </select>
        </div>

        <div class="chart-wrapper">
            {div_chart}
        </div>
    </div>

    <script src="assets/js/dashboard.js"></script>
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)