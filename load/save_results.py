import os


def save_table(df, path):
    """
    Guarda una tabla agregada pequeña en formato CSV.
    El procesamiento principal se realiza con PySpark.
    Pandas se usa solo para exportar resultados finales.
    """
    os.makedirs(path, exist_ok=True)

    file_name = path.split("/")[-1]
    output_path = os.path.join(path, f"{file_name}.csv")

    pandas_df = df.toPandas()
    pandas_df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Tabla guardada en: {output_path}")