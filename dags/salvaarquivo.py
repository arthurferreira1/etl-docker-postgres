from datetime import datetime, timedelta
from random import randint
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
import pandas as pd

# Configurações do PostgreSQL
postgres_conn_id = 'postgres_default'
postgres_db = 'airflow'
postgres_user = 'airflow'
postgres_password = 'airflow'
postgres_host = 'postgres'
postgres_port = 5432

# Configurações da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'example_postgres_dag',
    default_args=default_args,
    description='Uma DAG de exemplo para gerar dados e armazenar no PostgreSQL',
    schedule_interval=timedelta(days=1),  # Executar diariamente
)

# Função para gerar dados aleatórios
def generate_random_data(**kwargs):
    data = {
        'timestamp': [datetime.now() - timedelta(days=i) for i in range(10)],
        'value': [randint(1, 100) for _ in range(10)],
    }
    df = pd.DataFrame(data)
    return df

# Função para inserir dados no PostgreSQL
def insert_data_to_postgres(**kwargs):
    engine = create_engine(
        f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'
    )
    conn = engine.connect()
    
    # Obtenha o DataFrame gerado pela tarefa anterior
    task_instance = kwargs['ti']
    df = task_instance.xcom_pull(task_ids='generate_random_data_task')
    
    # Insira dados na tabela example_table
    df.to_sql('example_table', conn, index=False, if_exists='replace')
    
    # Feche a conexão
    conn.close()

# Tarefas da DAG
generate_random_data_task = PythonOperator(
    task_id='generate_random_data_task',
    python_callable=generate_random_data,
    provide_context=True,
    dag=dag,
)

insert_data_to_postgres_task = PythonOperator(
    task_id='insert_data_to_postgres_task',
    python_callable=insert_data_to_postgres,
    provide_context=True,
    dag=dag,
)

# Definir a ordem das tarefas
generate_random_data_task >> insert_data_to_postgres_task
