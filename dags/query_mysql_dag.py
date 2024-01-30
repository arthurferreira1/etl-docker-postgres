from datetime import datetime, timedelta
from airflow import DAG
from operators.custom_query_operator import CustomQueryOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('query_dag',
          default_args=default_args,
          description='Uma DAG para executar uma query e retornar dados',
          schedule_interval=timedelta(days=1),
          )

t1 = CustomQueryOperator(
    task_id='run_query',
    sql='SELECT * FROM sua_tabela',
    database_conn_id='seu_database_conn_id',
    dag=dag,
)

t1
