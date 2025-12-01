# Airflow Getting Started

Install `uv` with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart your shell or reload:

```bash
source ~/.profile
```

Create a `airflow` directory and `venv`:

```bash
mkdir airflow
cd airflow
uv python pin 3.11
uv venv
```

Install Apache Airflow:

```bash
AIRFLOW_VERSION=2.7.3
PYTHON_VERSION=3.11
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
uv pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

Create Airflow database:
```bash
export AIRFLOW_HOME=~/airflow
uv run airflow db init
```

Create a user:
```bash
uv run airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

Create a dag in `~/airflow/dags`. For example, this dag below runs `main.py` from a project `airflow_demo` on a minutely basis to extract bitcoin price:
```python
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
```

`~/airflow_demo/main.py`:
```python
import requests
from datetime import datetime

def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        return None

def log_price():
    price = get_bitcoin_price()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if price is not None:
        line = f"{now} - {price} USD\n"
    else:
        line = f"{now} - retrieval failed\n"
    with open("bitcoin_price.txt", "a") as f:
        f.write(line)
if __name__ == "__main__":
    log_price()
```

Check and test your dag:
```bash
uv run airflow dags list
uv run airflow tasks test <dag_id> <task_id> YYYY-MM-DDTHH:MM:SS
```

Start Scheduler:
```
uv run airflow scheduler
```

Monitor bitcoin price:
```bash
cat ../airflow_demo/bitcoin_price.txt
```