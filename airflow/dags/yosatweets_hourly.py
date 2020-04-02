import sys
sys.path.append("/home/airflow/yosatweets/airflow/package")
from yosatweets.common import *

dag = DAG(
    'yosatweets_hourly_v0.0',
    default_args=yosatweets.common.default_args,
    description='call funtion yosatweets_insert_tweets',
    start_date=days_ago(1),
    schedule_interval="00 *  *  *  *",
)

task1 = PythonOperator(
    task_id='yosatweets_insert_tweets',
    python_callable=yosatweets.common.exec_functions,
    provide_context=True,
    op_kwargs={"url": "https://us-central1-{}.cloudfunctions.net/yosatweets_insert_tweets".format(os.environ["GCP_PROJECT"])},
    dag=dag,
)

task1 # >> task2
