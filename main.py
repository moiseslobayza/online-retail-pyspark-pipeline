from pyspark.sql import SparkSession

from extract.load_data import load_retail_data
from transform.clean_data import clean_retail_data
from load.save_results import save_table

from analysis.business_metrics import (
    general_kpis,
    sales_by_country,
    monthly_sales,
    top_products_by_revenue,
    top_products_by_quantity,
    top_customers,
    date_range
)

from ml.customer_segmentation import (
    build_rfm_table,
    segment_customers,
    segment_summary
)


def main():

    # ============================================================
    # 1. INICIO DE SPARK
    # ============================================================
    # Se crea la SparkSession, que es el punto de entrada principal
    # para trabajar con DataFrames de PySpark.

    spark = SparkSession.builder \
        .appName("Online Retail Analysis") \
        .getOrCreate()

    path = "data/raw/online_retail.csv"


    # ============================================================
    # 2. EXTRACCIÓN / CARGA DE DATOS
    # ============================================================
    # Se carga el dataset original desde la carpeta data/raw/.

    df = load_retail_data(spark, path)

    print("DATOS ORIGINALES")
    df.show(5)
    df.printSchema()
    print("Filas originales:", df.count())


    # ============================================================
    # 3. LIMPIEZA Y TRANSFORMACIÓN
    # ============================================================
    # Se eliminan duplicados, nulos importantes, devoluciones,
    # cantidades/precios inválidos y se crean columnas nuevas como
    # TotalAmount, Year y Month.

    df_clean = clean_retail_data(df)

    print("DATOS LIMPIOS")
    df_clean.show(5)
    df_clean.printSchema()
    print("Filas limpias:", df_clean.count())


    # ============================================================
    # 4. ANÁLISIS EXPLORATORIO / MÉTRICAS DE NEGOCIO
    # ============================================================
    # Se calculan KPIs generales y métricas comerciales usando
    # agregaciones nativas de PySpark.

    kpis = general_kpis(df_clean)
    country_sales = sales_by_country(df_clean)
    sales_monthly = monthly_sales(df_clean)
    products_revenue = top_products_by_revenue(df_clean)
    products_quantity = top_products_by_quantity(df_clean)
    customers_top = top_customers(df_clean)
    dates = date_range(df_clean)

    print("KPIs GENERALES")
    kpis.show()

    print("VENTAS POR PAIS")
    country_sales.show(10)

    print("VENTAS MENSUALES")
    sales_monthly.show(50)

    print("TOP PRODUCTOS POR FACTURACION")
    products_revenue.show(10, truncate=False)

    print("TOP PRODUCTOS POR CANTIDAD")
    products_quantity.show(10, truncate=False)

    print("TOP CLIENTES")
    customers_top.show(10)

    print("RANGO DE FECHAS DEL DATASET")
    dates.show()


    # ============================================================
    # 5. EXPORTACIÓN DE RESULTADOS DEL EDA
    # ============================================================
    # Se guardan las tablas agregadas del análisis exploratorio.
    # El procesamiento se hizo con PySpark; la exportación final
    # usa save_table para generar archivos CSV de salida.

    save_table(kpis, "outputs/tables/general_kpis")
    save_table(country_sales, "outputs/tables/sales_by_country")
    save_table(sales_monthly, "outputs/tables/monthly_sales")
    save_table(products_revenue, "outputs/tables/top_products_by_revenue")
    save_table(products_quantity, "outputs/tables/top_products_by_quantity")
    save_table(customers_top, "outputs/tables/top_customers")


    # ============================================================
    # 6. CONSTRUCCIÓN DE VARIABLES RFM
    # ============================================================
    # Se construye una tabla por cliente con:
    # Recency: días desde la última compra
    # Frequency: cantidad de facturas
    # Monetary: monto total comprado

    print("TABLA RFM")
    rfm = build_rfm_table(df_clean)
    rfm.show(10)


    # ============================================================
    # 7. SEGMENTACIÓN DE CLIENTES CON SPARK MLLIB
    # ============================================================
    # Se aplica KMeans sobre las variables RFM para agrupar clientes
    # en segmentos comerciales.

    print("SEGMENTACION DE CLIENTES CON KMEANS")
    segmented_customers = segment_customers(rfm, k=4)
    segmented_customers.show(10)


    # ============================================================
    # 8. RESUMEN DE SEGMENTOS
    # ============================================================
    # Se resumen los segmentos obtenidos para interpretar el perfil
    # promedio de cada grupo de clientes.

    print("RESUMEN DE SEGMENTOS")
    segments = segment_summary(segmented_customers)
    segments.show()


    # ============================================================
    # 9. EXPORTACIÓN DE RESULTADOS DE MACHINE LEARNING
    # ============================================================
    # Se guardan la tabla RFM, los clientes segmentados y el resumen
    # de segmentos.

    save_table(rfm, "outputs/tables/rfm_customers")
    save_table(segmented_customers, "outputs/tables/segmented_customers")
    save_table(segments, "outputs/tables/segment_summary")


    # ============================================================
    # 10. CIERRE DE SPARK
    # ============================================================
    # Se cierra la sesión de Spark para liberar recursos.

    spark.stop()


if __name__ == "__main__":
    main()