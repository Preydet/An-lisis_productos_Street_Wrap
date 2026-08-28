/**
 * Títulos para cada una de las vistas
 */
const TITULOS_VISTAS = [
    "<b>Top 20 Productos Más Vendidos</b>",
    "<b>Top 20 Platos Principales (Excluye *Extra)</b>",
    "<b>Top 20 Ingredientes e Extras Más Vendidos</b>",
    "<b>Ventas de Categoría: Base / Proteínas</b>",
    "<b>Ventas de Categoría: Granos / Legumbres</b>",
    "<b>Ventas de Categoría: Verduras</b>",
    "<b>Ventas de Categoría: Toppings</b>",
    "<b>Ventas de Categoría: Salsas</b>",
    "<b>Top 50 Productos Más Vendidos</b>"
];

/**
 * Alterna la vista activa de Plotly y redimensiona dinámicamente el contenedor
 */
function switchView(selectedIndex) {
    const chartDiv = document.getElementById('sales_plotly_div');
    if (!chartDiv || !chartDiv.data) return;

    const idx = parseInt(selectedIndex, 10) || 0;
    const totalTraces = chartDiv.data.length;
    const targetIdx = (idx >= 0 && idx < totalTraces) ? idx : 0;

    // 1. Mostrar únicamente la traza seleccionada
    const visibilityMap = new Array(totalTraces).fill(false);
    visibilityMap[targetIdx] = true;

    // 2. Ajustar altura dinámicamente según la cantidad de ítems
    const activeTrace = chartDiv.data[targetIdx];
    const itemCount = activeTrace && activeTrace.y ? activeTrace.y.length : 10;
    const isMobile = window.innerWidth <= 600;
    
    // Asignación de px por barra para dar espacio suficiente a listas largas como Top 50
    const pxPorBarra = isMobile ? 28 : 32;
    const paddingExtra = 100; // Margen para títulos y eje X
    const targetHeight = Math.max(isMobile ? 450 : 500, (itemCount * pxPorBarra) + paddingExtra);

    // 3. Aplicar cambios en Plotly
    Plotly.restyle(chartDiv, { visible: visibilityMap });

    Plotly.relayout(chartDiv, {
        'title.text': TITULOS_VISTAS[targetIdx] || TITULOS_VISTAS[0],
        'height': targetHeight,
        'autosize': true,
        'margin.l': isMobile ? 140 : 220,
        'margin.r': 30,
        'margin.t': 50,
        'margin.b': 50
    }).then(() => {
        // Fuerza a Plotly a re-calcular límites del canvas sin requerir zoom manual
        Plotly.Plots.resize(chartDiv);
    });
}

// Escuchar cambios de tamaño de ventana de forma adaptativa
window.addEventListener('resize', function () {
    const selector = document.getElementById('categorySelector');
    if (selector) {
        switchView(selector.value);
    }
});