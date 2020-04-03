## 前提
- gceのf1-micro
- osはUbuntu-18.04
- ユーザー名はairflow

## 導入
以下を実行。pythonは3.5.3以降が必須（https://github.com/pydata/xarray/issues/2866）。
```
# installまで
sudo apt update
sudo apt -y install python3.7 python3-pip
pip3 install --upgrade apache-airflow requests

# githubからpull
git clone https://github.com/dr666m1/project_yosatweets.git $HOME/yosatweets
```
`$HOME/yosatweets/airflow/dags/yosatweets_config.py`で`sandbox_token`と`gcp_project`を設定すること。
完了したら一度シェルを再起動。
```
airflow initdb
cp $HOME/yosatweets/airflow/airflow.cfg $HOME/airflow/airflow.cfg
mkdir -p $HOME/airflow/dags
ln -s $HOME/yosatweets/airflow/dags $HOME/airflow/dags/yosatweets
sudo ln -s $HOME/yosatweets/airflow/airflow-scheduler.service /etc/systemd/system/airflow-scheduler.service
sudo systemctl enable airflow-scheduler
sudo systemctl start airflow-scheduler
```

