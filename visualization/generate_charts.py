from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent.parent

TABLES_DIR = BASE_DIR / "outputs" / "tables"
CHARTS_DIR = BASE_DIR / "outputs" / "charts"

CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def load_table(folder_name, file_name):
    path = TABLES_DIR / folder_name / file_name
    return pd.read_csv(path)


def chart_monthly_sales():
    df = load_table("monthly_sales", "monthly_sales.csv")

    df["Period"] = df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2)
    df["Period"] = pd.to_datetime(df["Period"])

    plt.figure(figsize=(10, 5))
    plt.plot(df["Period"], df["MonthlySales"], marker="o")
    plt.title("Evolución mensual de ventas")
    plt.xlabel("Mes")
    plt.ylabel("Ventas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "monthly_sales.png", dpi=300)
    plt.close()


def chart_sales_by_country():
    df = load_table("sales_by_country", "sales_by_country.csv").head(10)
    df = df.sort_values("TotalSales", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["Country"], df["TotalSales"])
    plt.title("Top 10 países por ventas")
    plt.xlabel("Ventas")
    plt.ylabel("País")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "sales_by_country.png", dpi=300)
    plt.close()


def chart_top_products_revenue():
    df = load_table("top_products_by_revenue", "top_products_by_revenue.csv").head(10)
    df = df.sort_values("Revenue", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["Description"], df["Revenue"])
    plt.title("Top 10 productos por facturación")
    plt.xlabel("Facturación")
    plt.ylabel("Producto")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "top_products_by_revenue.png", dpi=300)
    plt.close()


def chart_top_products_quantity():
    df = load_table("top_products_by_quantity", "top_products_by_quantity.csv").head(10)
    df = df.sort_values("TotalQuantity", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["Description"], df["TotalQuantity"])
    plt.title("Top 10 productos por cantidad vendida")
    plt.xlabel("Cantidad vendida")
    plt.ylabel("Producto")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "top_products_by_quantity.png", dpi=300)
    plt.close()


def chart_top_customers():
    df = load_table("top_customers", "top_customers.csv").head(10)
    df["CustomerID"] = df["CustomerID"].astype(int).astype(str)
    df = df.sort_values("CustomerRevenue", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["CustomerID"], df["CustomerRevenue"])
    plt.title("Top 10 clientes por facturación")
    plt.xlabel("Facturación")
    plt.ylabel("Cliente")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "top_customers.png", dpi=300)
    plt.close()


def chart_sales_by_country_without_uk():
    df = load_table("sales_by_country", "sales_by_country.csv")

    df = df[df["Country"] != "United Kingdom"].head(10)
    df = df.sort_values("TotalSales", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["Country"], df["TotalSales"])
    plt.title("Top 10 países por ventas sin United Kingdom")
    plt.xlabel("Ventas")
    plt.ylabel("País")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "sales_by_country_without_uk.png", dpi=300)
    plt.close()

def chart_monthly_sales_complete_months():
    df = load_table("monthly_sales", "monthly_sales.csv")

    # Excluimos diciembre 2011 porque el dataset llega solo hasta el día 9
    df = df[~((df["Year"] == 2011) & (df["Month"] == 12))]

    df["Period"] = df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2)
    df["Period"] = pd.to_datetime(df["Period"])

    plt.figure(figsize=(10, 5))
    plt.plot(df["Period"], df["MonthlySales"], marker="o")
    plt.title("Evolución mensual de ventas sin meses incompletos")
    plt.xlabel("Mes")
    plt.ylabel("Ventas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "monthly_sales_complete_months.png", dpi=300)
    plt.close()
    
    
def chart_segment_customers():
    df = load_table("segment_summary", "segment_summary.csv")
    df["Segment"] = df["Segment"].astype(str)

    plt.figure(figsize=(8, 5))
    plt.bar(df["Segment"], df["Customers"])
    plt.title("Cantidad de clientes por segmento")
    plt.xlabel("Segmento")
    plt.ylabel("Cantidad de clientes")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "segment_customers.png", dpi=300)
    plt.close()


def chart_segment_avg_monetary():
    df = load_table("segment_summary", "segment_summary.csv")
    df["Segment"] = df["Segment"].astype(str)

    plt.figure(figsize=(8, 5))
    plt.bar(df["Segment"], df["AvgMonetary"])
    plt.title("Facturación promedio por segmento")
    plt.xlabel("Segmento")
    plt.ylabel("Monetary promedio")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "segment_avg_monetary.png", dpi=300)
    plt.close()


def chart_segment_avg_frequency():
    df = load_table("segment_summary", "segment_summary.csv")
    df["Segment"] = df["Segment"].astype(str)

    plt.figure(figsize=(8, 5))
    plt.bar(df["Segment"], df["AvgFrequency"])
    plt.title("Frecuencia promedio por segmento")
    plt.xlabel("Segmento")
    plt.ylabel("Frequency promedio")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "segment_avg_frequency.png", dpi=300)
    plt.close()


def chart_segment_avg_recency():
    df = load_table("segment_summary", "segment_summary.csv")
    df["Segment"] = df["Segment"].astype(str)

    plt.figure(figsize=(8, 5))
    plt.bar(df["Segment"], df["AvgRecency"])
    plt.title("Recency promedio por segmento")
    plt.xlabel("Segmento")
    plt.ylabel("Recency promedio (días)")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "segment_avg_recency.png", dpi=300)
    plt.close()



def main():
    chart_monthly_sales()
    chart_sales_by_country()
    chart_sales_by_country_without_uk()
    chart_top_products_revenue()
    chart_top_products_quantity()
    chart_top_customers()
    chart_monthly_sales_complete_months()
    
    chart_segment_customers()
    chart_segment_avg_monetary()
    chart_segment_avg_frequency()
    chart_segment_avg_recency()

    print("Gráficos generados en outputs/charts/")


if __name__ == "__main__":
    main()