import sys
sys.path.append("/home/airflow/yosatweets/airflow/package")
from package.yosatweets_common import *

dag = DAG(
    'yosatweets_test_v0.1',
    default_args=common_args,
    description='test',
    start_date=days_ago(1),
    schedule_interval="20 *  *  *  *",
)

task1 = BashOperator(
    task_id='yosatweets_test',
    bash_command="date > /home/airflow/yosatweets_test.log",
    dag=dag,
)

task1 # >> task2
