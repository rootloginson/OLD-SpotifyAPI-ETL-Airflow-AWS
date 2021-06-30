from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import spotify_app


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0,0,0,0,0),
    'email': 'airflow@githubexample.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
    }

dag = DAG(
    'spotify_app_dag',
    default_args=default_args,
    description='Everyday_New_Random_Track',
    schedule_interval=timedelta(days=1) #how often run, daily
    )

run_etl = PythonOperator(
    task_id='Task_spotify_app',
    python_callable = spotify_app.run_spotify_app,
    dag = dag
    )

run_etl
