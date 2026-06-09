from datetime import datetime
from pathlib import Path
import os

from airflow import DAG
from airflow.operators.bash import BashOperator


# Ruta del proyecto:
# 1) Usa variable de entorno si existe
# 2) Si no, asume que dags/ está dentro del proyecto
PROJECT_PATH = os.environ.get(
    "ONLINE_RETAIL_PROJECT_PATH",
    str(Path(__file__).resolve().parents[1])
)

# Comando Python configurable
PYTHON_CMD = os.environ.get("ONLINE_RETAIL_PYTHON_CMD", "python")


with DAG(
    dag_id="online_retail_pipeline",
    description="Orquestación simple del pipeline Online Retail con PySpark",
    start_date=datetime(2026, 6, 1),
    schedule=None,
    catchup=False,
    tags=["pyspark", "retail", "airflow"],
) as dag:

    run_pyspark_pipeline = BashOperator(
        task_id="run_pyspark_pipeline",
        bash_command=f'cd "{PROJECT_PATH}" && {PYTHON_CMD} main.py'
    )

    generate_charts = BashOperator(
        task_id="generate_charts",
        bash_command=f'cd "{PROJECT_PATH}" && {PYTHON_CMD} visualization/generate_charts.py'
    )

    run_pyspark_pipeline >> generate_charts