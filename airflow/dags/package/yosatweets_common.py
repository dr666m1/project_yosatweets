from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
import requests
import os
from datetime import timedelta

def exec_functions(url, token, task, task_instance, **kwargs):
    payload = {}
    res = requests.post(url, data=payload)
    if res.status_code//100 != 2:
        msg = "error report\nid: {}\nn-th: {}".format(task.task_id, task_instance.try_number)
        send_line_msg(msg, token)
        raise Exception("response status code is not in 200 - 299\n{}".format(res.text))

def send_line_msg(msg, token):
    try:
        url = "https://notify-api.line.me/api/notify"
        payload = {"message": msg}
        headers = {"Authorization": "Bearer {}".format(token)}
        requests.post(url, data=payload, headers=headers)
    except KeyError as e:
        print(e)

common_args = {
    'owner': os.environ.get("USER", "unknown"),
    'depends_on_past': False,
    #'start_date': days_ago(7),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}
