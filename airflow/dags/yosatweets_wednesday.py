import sys
sys.path.append("/home/airflow/yosatweets/airflow/package")
from yosatweets.common import *

dag = DAG(
    'yosatweets_wednesday_v0.0',
    default_args=yosatweets.common.default_args,
    description='call funtion yosatweets_plot_wordcloud',
    start_date=days_ago(7),
    schedule_interval="00 00 *  *  wed",
)

task1 = PythonOperator(
    task_id='yosatweets_plot_wordcloud',
    python_callable=yosatweets.common.exec_functions,
    provide_context=True,
    op_kwargs={"url": "https://us-central1-{}.cloudfunctions.net/yosatweets_plot_wordcloud".format(os.environ["GCP_PROJECT"])},
    dag=dag,
)

task1 # >> task2
