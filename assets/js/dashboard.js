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
 * Recorta textos largos para evitar desbordamientos
 */
function acortarTexto(texto, maxCaracteres) {
    if (!texto) return '';
    const str = String(texto);
    return str.length > maxCaracteres ? str.substring(0, maxCaracteres - 3) + '...' : str;
}

/**
 * Alterna la vista seleccionada de forma segura
 */
function switchView(selectedIndex) {
    const chartDiv = document.getElementById('sales_plotly_div');
    if (!chartDiv || !chartDiv.data) return;

    const idx = parseInt(selectedIndex, 10) || 0;
    const totalTraces = chartDiv.data.length;

    // 1. Crear mapa booleano de visibilidad
    const visibilityMap = new Array(totalTraces).fill(false);
    const targetIdx = (idx >= 0 && idx < totalTraces) ? idx : 0;
    visibilityMap[targetIdx] = true;

    // 2. Obtener la traza activa
    const activeTrace = chartDiv.data[targetIdx];
    const itemCount = activeTrace && activeTrace.y ? activeTrace.y.length : 10;

    // 3. Truncar nombres largos si no han sido procesados
    const isMobile = window.innerWidth <= 600;
    const maxChars = isMobile ? 22 : 35;

    if (activeTrace && activeTrace.y) {
        if (!activeTrace._labelsOriginales) {
            activeTrace._labelsOriginales = [...activeTrace.y];
        }
        activeTrace.y = activeTrace._labelsOriginales.map(label => acortarTexto(label, maxChars));
    }

    // 4. Calcular altura adecuada por cantidad de barras
    const pxPorBarra = isMobile ? 26 : 30;
    const targetHeight = Math.max(isMobile ? 450 : 500, itemCount * pxPorBarra);

    // 5. Aplicar cambios a Plotly
    Plotly.restyle(chartDiv, { visible: visibilityMap });

    Plotly.relayout(chartDiv, {
        'title.text': TITULOS_VISTAS[targetIdx] || TITULOS_VISTAS[0],
        'height': targetHeight,
        'autosize': true,
        'margin.l': isMobile ? 140 : 250,
        'margin.r': 30,
        'margin.t': 50,
        'margin.b': 50,
        'yaxis.automargin': true,
        'xaxis.automargin': true
    });
}

// Redimensionar responsivamente
window.addEventListener('resize', function () {
    const selector = document.getElementById('categorySelector');
    if (selector) {
        switchView(selector.value);
    }
});