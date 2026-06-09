import pandas as pd

archivo_excel = "data/raw/online_retail.xlsx"

hojas = pd.read_excel(archivo_excel, sheet_name=None)

dataframes = []

for nombre_hoja, df in hojas.items():
    df["PeriodoFuente"] = nombre_hoja
    dataframes.append(df)

df_total = pd.concat(dataframes, ignore_index=True)

df_total.to_csv("data/raw/online_retail.csv", index=False, encoding="utf-8")

print("Conversión finalizada.")
print(f"Filas totales: {len(df_total)}")