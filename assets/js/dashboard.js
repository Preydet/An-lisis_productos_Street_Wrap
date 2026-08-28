function switchView(selectedIndex, counts) {
    const chartDiv = document.getElementById('sales_plotly_div');
    if (!chartDiv) return;

    const idx = parseInt(selectedIndex);
    const totalTraces = 9;

    // Crear mapa de visibilidad booleano
    const visibilityMap = Array(totalTraces).fill(false);
    visibilityMap[idx] = true;

    const titles = [
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

    // Cálculo dinámico de altura para que las barras nunca se aprieten
    const calcHeight = (count, minH = 500) => Math.max(minH, (count || 10) * 28);

    const heights = [
        600,
        600,
        600,
        calcHeight(counts.base),
        calcHeight(counts.granos),
        calcHeight(counts.verduras),
        calcHeight(counts.toppings),
        calcHeight(counts.salsas),
        1100
    ];

    Plotly.restyle(chartDiv, { visible: visibilityMap });

    Plotly.relayout(chartDiv, {
        'title.text': titles[idx],
        'height': heights[idx]
    });
}