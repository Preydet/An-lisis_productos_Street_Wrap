"""
Módulo para generación y exportación del reporte HTML final
"""
from dashboard_builder import DashboardBuilder

class InteractiveReporter:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.builder = DashboardBuilder(analyzer)

    def build_dashboard_html(self, output_path: str):
        """Renderiza el gráfico dinámico en una plantilla HTML modularizada."""
        fig, len_df_base = self.builder.create_sales_chart()
        div_chart = fig.to_html(full_html=False, include_plotlyjs='cdn', div_id="sales_plotly_div")
        base_height = max(500, len_df_base * 28)

        html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Interactivo de Ventas</title>
    <!-- Vinculación con assets/css/styles.css -->
    <link rel="stylesheet" href="../assets/css/styles.css">
</head>
<body>
    <div class="container">
        <h1>📦 Reporte Interactivo de Ventas por Producto</h1>
        
        <div class="filter-container">
            <span class="filter-label">🔍 Seleccionar Categoría / Vista:</span>
            <select id="categorySelector" class="filter-select" onchange="switchView(this.value, {base_height})">
                <option value="0">📊 Top 20 General</option>
                <option value="1">🥗 Solo Platos Principales (Sin *Extra)</option>
                <option value="2">🧀 Solo Ingredientes y Acompañamientos (*Extra)</option>
                <option value="3">🥩 Solo Categoría Base</option>
                <option value="4">📋 Top 50 General</option>
            </select>
        </div>

        <div class="chart-wrapper">
            {div_chart}
        </div>
    </div>

    <!-- Vinculación con assets/js/dashboard.js -->
    <script src="../assets/js/dashboard.js"></script>
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)