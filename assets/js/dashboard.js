function switchView(selectedIndex, baseHeight) {
    const chartDiv = document.getElementById('sales_plotly_div');
    if (!chartDiv) return;

    const idx = parseInt(selectedIndex);

    // Visibilidad de trazas: Top20, SinExtras, SoloExtras, SoloBase, Top50
    const visibilityMap = [
        [true, false, false, false, false],  // Top 20 General
        [false, true, false, false, false],  // Sin Extras
        [false, false, true, false, false],  // Solo Extras
        [false, false, false, true, false],  // Solo Base
        [false, false, false, false, true]   // Top 50
    ];

    const titles = [
        "<b>Top 20 Productos Más Vendidos</b>",
        "<b>Top 20 Platos Principales (Excluye *Extra)</b>",
        "<b>Top 20 Ingredientes e Extras Más Vendidos</b>",
        "<b>Ventas de Productos de la Categoría Base</b>",
        "<b>Top 50 Productos Más Vendidos</b>"
    ];

    const heights = [600, 600, 600, baseHeight || 600, 1100];

    // Actualiza visibilidad
    Plotly.restyle(chartDiv, { visible: visibilityMap[idx] });

    // Actualiza layout
    Plotly.relayout(chartDiv, {
        'title.text': titles[idx],
        'height': heights[idx]
    });
}