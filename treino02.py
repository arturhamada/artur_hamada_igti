# Primeira DAG do Aiirflow

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd


# Argumentos default

default_args = {
    'owner' : 'Hamada',
    'depends_on_past': False,
    'start_date': datetime(2020,12,22, 10, 00),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}


## Definicao da DAG - fluxo
dag = DAG(
    "treino-02",
    description="Extraidados do Titanic da interrnet calcula a idade média",
    default_args=default_args,
    schedule_interval="*/2 * * * *"
)

get_data = BashOperator(
    task_id='get-data',
    bash_command='curl https://raw.githubusercontent.com/A3Data/hermione/master/hermione/file_text/train.csv -o ~/train.csv',
    dag=dag
)

def calculate_mean_age():
    df = pd.read_csv('~/train.csv')
    med = df.Age.mean()
    return med

def print_age(**context):
    value = context['task_instance'].xcom_pull(task_ids='calcula-idade-media')
    print(f"A idade media do Titanic era {value} anos.")

task_idade_media = PythonOperator(
    task_id='calcula-idade-media',
    python_callable=calculate_mean_age,
    dag=dag
)

task_print_idade = PythonOperator(
    task_id='mostra-idade',
    python_callable=print_age,
    provide_context=True,
    dag=dag
)

get_data >> task_idade_media >> task_print_idade
