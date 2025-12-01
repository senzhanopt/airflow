from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="run_bitcoin_bash",
    start_date=datetime(2025, 11, 30, 21, 30),
    schedule_interval="* * * * *",
    catchup=False,
) as dag:

    run_task = BashOperator(
        task_id="run_bitcoin",
        bash_command="""
        cd /home/en_han/airflow_demo
        uv run main.py
        """
    )
