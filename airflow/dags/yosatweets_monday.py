import sys
sys.path.append("/home/airflow/yosatweets/airflow/package")
from yosatweets.common import *

dag = DAG(
    'yosatweets_monday_v0.0',
    default_args=common_args,
    description='call funtion yosatweets_count_tweets, yosatweets_plot_line_chart',
    start_date=days_ago(7),
    schedule_interval="00 00 *  *  mon",
)

task1 = PythonOperator(
    task_id='yosatweets_count_tweets',
    python_callable=exec_functions,
    provide_context=True,
    op_kwargs={"url": "https://us-central1-{}.cloudfunctions.net/yosatweets_count_tweets".format(os.environ["GCP_PROJECT"])},
    dag=dag,
)

task2 = PythonOperator(
    task_id='yosatweets_plot_line_chart',
    python_callable=exec_functions,
    provide_context=True,
    op_kwargs={"url": "https://us-central1-{}.cloudfunctions.net/yosatweets_plot_line_chart".format(os.environ["GCP_PROJECT"])},
    dag=dag,
)

task1 >> task2
