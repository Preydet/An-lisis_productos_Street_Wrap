"""
Punto de Entrada Principal (Main Execution Pipeline)
"""
import sys
from pathlib import Path

# Agregar src/ al path para importaciones limpias
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from config import DEFAULT_CSV_PATH, OUTPUT_HTML_REPORT
from data_loader import DataLoader
from analyzer import SalesAnalyzer
from reporter import InteractiveReporter

def main():
    print("=== INICIANDO ANÁLISIS DE CANTIDAD DE VENTAS POR PRODUCTO ===")

    # 1. Cargar y limpiar los datos
    loader = DataLoader(DEFAULT_CSV_PATH)
    df_raw = loader.load_raw_data()
    df_clean = loader.clean_data(df_raw)

    # 2. Analizar y obtener métricas
    analyzer = SalesAnalyzer(df_clean)
    top_10 = analyzer.get_top_products(10)

    print("\n--- TOP 10 PRODUCTOS MÁS VENDIDOS ---")
    print(top_10.to_string(index=False))

    # 3. Generar el reporte interactivo en HTML
    reporter = InteractiveReporter(analyzer)
    reporter.build_dashboard_html(OUTPUT_HTML_REPORT, top_n=20)

    print(f"\n[OK] Reporte generado exitosamente en: {OUTPUT_HTML_REPORT}")
    print("=== PROCESO FINALIZADO ===")

if __name__ == "__main__":
    main()