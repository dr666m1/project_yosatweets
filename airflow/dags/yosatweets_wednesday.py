import sys
sys.path.append("/home/airflow/yosatweets/airflow/package")
from package.yosatweets_common import *
from package.yosatweets_config import *

dag = DAG(
    'yosatweets_wednesday_v0.1',
    default_args=common_args,
    description='call funtion yosatweets_plot_wordcloud',
    start_date=days_ago(7),
    schedule_interval="00 00 *  *  wed",
)

task1 = PythonOperator(
    task_id='yosatweets_plot_wordcloud',
    python_callable=exec_functions,
    provide_context=True,
    op_kwargs={
        "url": "https://us-central1-{}.cloudfunctions.net/yosatweets_plot_wordcloud".format(gcp_project),
        "token": sandbox_token
    },
    dag=dag,
)

task1 # >> task2
