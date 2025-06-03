from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1),
    'catchup': False
}

with DAG(
    dag_id='test_spark',
    default_args=default_args,
    schedule_interval=None,
    description='DAG de test pour SparkSubmitOperator',
    tags=['spark', 'test']
) as dag:

    test_spark = SparkSubmitOperator(
        task_id='test_spark_task',
        application='/opt/airflow/dags/scripts/test_spark_.py',  # Ce script sera lancé
        conn_id='test_spark',  # Remplace si tu as donné un autre ID à la connexion Spark
        verbose=True
    )
