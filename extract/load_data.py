def load_retail_data(spark, path):
    """
    Carga el dataset Online Retail usando PySpark.
    """
    df = spark.read.csv(
        path,
        header=True,
        inferSchema=True
    )
    return df