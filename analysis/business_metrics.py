from pyspark.sql.functions import sum as spark_sum, countDistinct, count, avg, desc, round, col, min as spark_min, max as spark_max


def general_kpis(df):
    return df.agg(
        round(spark_sum("TotalAmount"), 2).alias("TotalSales"),
        countDistinct("Invoice").alias("TotalInvoices"),
        countDistinct("CustomerID").alias("UniqueCustomers"),
        countDistinct("StockCode").alias("UniqueProducts"),
        round(avg("TotalAmount"), 2).alias("AvgLineAmount")
    )


def sales_by_country(df):
    return df.groupBy("Country") \
        .agg(round(spark_sum("TotalAmount"), 2).alias("TotalSales")) \
        .orderBy(desc("TotalSales"))


def monthly_sales(df):
    return df.groupBy("Year", "Month") \
        .agg(round(spark_sum("TotalAmount"), 2).alias("MonthlySales")) \
        .orderBy("Year", "Month")


def top_products_by_revenue(df):
    return df.groupBy("StockCode", "Description") \
        .agg(round(spark_sum("TotalAmount"), 2).alias("Revenue")) \
        .orderBy(desc("Revenue"))


def top_products_by_quantity(df):
    return df.groupBy("StockCode", "Description") \
        .agg(spark_sum("Quantity").alias("TotalQuantity")) \
        .orderBy(desc("TotalQuantity"))


def top_customers(df):
    return df.filter(col("CustomerID").isNotNull()) \
        .groupBy("CustomerID") \
        .agg(round(spark_sum("TotalAmount"), 2).alias("CustomerRevenue")) \
        .orderBy(desc("CustomerRevenue"))


def date_range(df):
    return df.agg(
        spark_min("InvoiceDate").alias("FechaMinima"),
        spark_max("InvoiceDate").alias("FechaMaxima")
    )

