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

// Texto estático del subtítulo KPI dibujado directo en Plotly
const SUBTITULO_KPI = "<br><span style='font-size: 13px; color: #1e3c72;'>📋 Total de Pedidos a la Fecha: <b>11,617</b></span>";

/**
 * Alterna la vista activa de Plotly manteniendo el subtítulo estático del total de pedidos
 */
function switchView(selectedIndex) {
    const chartDiv = document.getElementById('sales_plotly_div');
    if (!chartDiv || !chartDiv.data) return;

    const idx = parseInt(selectedIndex, 10) || 0;
    const totalTraces = chartDiv.data.length;
    const targetIdx = (idx >= 0 && idx < totalTraces) ? idx : 0;

    // 1. Visibilidad
    const visibilityMap = new Array(totalTraces).fill(false);
    visibilityMap[targetIdx] = true;

    // 2. Cálculo de altura
    const activeTrace = chartDiv.data[targetIdx];
    const itemCount = activeTrace && activeTrace.y ? activeTrace.y.length : 10;
    const isMobile = window.innerWidth <= 600;
    const pxPorBarra = isMobile ? 28 : 32;
    const targetHeight = Math.max(isMobile ? 450 : 500, (itemCount * pxPorBarra) + 100);

    // 3. Aplicar visibilidad
    Plotly.restyle(chartDiv, { visible: visibilityMap });

    // 4. Actualizar título (con Subtítulo KPI) y layout
    const tituloCompleto = (TITULOS_VISTAS[targetIdx] || TITULOS_VISTAS[0]) + SUBTITULO_KPI;

    Plotly.relayout(chartDiv, {
        'title.text': tituloCompleto,
        'height': targetHeight,
        'autosize': true,
        'margin.l': isMobile ? 140 : 220,
        'margin.r': 120,
        'margin.t': 80,
        'margin.b': 50
    }).then(() => {
        Plotly.Plots.resize(chartDiv);
    });
}

// Redimensionar responsivamente
window.addEventListener('resize', function () {
    const selector = document.getElementById('categorySelector');
    if (selector) {
        switchView(selector.value);
    }
});