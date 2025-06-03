from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def check_minio_via_http():
    hook = S3Hook(aws_conn_id='minio_con')
    bucket = 'bronze'  

    if not hook.check_for_bucket(bucket):
        raise Exception(f"Bucket '{bucket}' non trouvé.")
    
    keys = hook.list_keys(bucket)
    print(f"Fichiers dans {bucket} : {keys or 'aucun'}")

with DAG(
    dag_id='test_minio_http_conn',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:
    test_task = PythonOperator(
        task_id='check_minio_http',
        python_callable=check_minio_via_http,
    )

