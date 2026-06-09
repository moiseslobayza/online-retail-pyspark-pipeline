from pyspark.sql.functions import (
    col,
    max as spark_max,
    sum as spark_sum,
    countDistinct,
    count,
    avg,
    round,
    datediff,
    lit,
    when
)

from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans


def build_rfm_table(df):
    """
    Construye tabla RFM por cliente:
    Recency: días desde última compra
    Frequency: cantidad de facturas
    Monetary: facturación total
    """

    reference_date = df.agg(spark_max("InvoiceDate")).collect()[0][0]

    rfm = df.groupBy("CustomerID").agg(
        spark_max("InvoiceDate").alias("LastPurchaseDate"),
        countDistinct("Invoice").alias("Frequency"),
        round(spark_sum("TotalAmount"), 2).alias("Monetary")
    )

    rfm = rfm.withColumn(
        "Recency",
        datediff(lit(reference_date), col("LastPurchaseDate"))
    )

    rfm = rfm.select(
        "CustomerID",
        "Recency",
        "Frequency",
        "Monetary"
    )

    return rfm


def segment_customers(rfm, k=4):
    """
    Segmenta clientes usando KMeans de Spark MLlib.
    """

    assembler = VectorAssembler(
        inputCols=["Recency", "Frequency", "Monetary"],
        outputCol="features"
    )

    assembled = assembler.transform(rfm)

    scaler = StandardScaler(
        inputCol="features",
        outputCol="scaled_features",
        withStd=True,
        withMean=True
    )

    scaler_model = scaler.fit(assembled)
    scaled_data = scaler_model.transform(assembled)

    kmeans = KMeans(
        featuresCol="scaled_features",
        predictionCol="Segment",
        k=k,
        seed=42
    )

    model = kmeans.fit(scaled_data)
    segmented = model.transform(scaled_data)
    
    segmented = segmented.withColumn(
    "SegmentName",
    when(col("Segment") == 0, "Base activa")
    .when(col("Segment") == 1, "Ultra VIP")
    .when(col("Segment") == 2, "Inactivos / bajo valor")
    .when(col("Segment") == 3, "Premium recurrentes")
    .otherwise("Sin clasificar")
    )

    return segmented.select(
        "CustomerID",
        "Recency",
        "Frequency",
        "Monetary",
        "Segment",
        "SegmentName"
    )


def segment_summary(segmented):
    """
    Resume las características promedio de cada segmento.
    """

    return segmented.groupBy("Segment", "SegmentName").agg(
    count("CustomerID").alias("Customers"),
    round(avg("Recency"), 2).alias("AvgRecency"),
    round(avg("Frequency"), 2).alias("AvgFrequency"),
    round(avg("Monetary"), 2).alias("AvgMonetary")
    ).orderBy("Segment")