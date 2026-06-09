from pyspark.sql.functions import col, year, month, round


def clean_retail_data(df):
    df = df.withColumnRenamed("Customer ID", "CustomerID")

    df_clean = df.dropDuplicates()

    df_clean = df_clean.filter(col("Invoice").isNotNull())
    df_clean = df_clean.filter(col("StockCode").isNotNull())
    df_clean = df_clean.filter(col("Description").isNotNull())
    df_clean = df_clean.filter(col("InvoiceDate").isNotNull())
    df_clean = df_clean.filter(col("Country").isNotNull())
    df_clean = df_clean.filter(col("CustomerID").isNotNull())

    # Quitamos devoluciones/cancelaciones y valores inválidos
    df_clean = df_clean.filter(~col("Invoice").startswith("C"))
    df_clean = df_clean.filter(col("Quantity") > 0)
    df_clean = df_clean.filter(col("Price") > 0)

    # Columna de facturación
    df_clean = df_clean.withColumn(
        "TotalAmount",
        round(col("Quantity") * col("Price"), 2)
    )

    # Variables temporales
    df_clean = df_clean.withColumn("Year", year(col("InvoiceDate")))
    df_clean = df_clean.withColumn("Month", month(col("InvoiceDate")))

    return df_clean