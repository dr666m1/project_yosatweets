from yosatweets.common import *

dag = DAG(
    'yosatweets_test_v0.0',
    default_args=yosatweets.common.default_args,
    description='test',
    start_date=days_ago(1),
    schedule_interval="00 *  *  *  *",
)

task1 = BashOperator(
    task_id='yosatweets_test',
    bash_command="date > /home/airflow/tmp/yosatweets_test.log",
    dag=dag,
)

task1 # >> task2
