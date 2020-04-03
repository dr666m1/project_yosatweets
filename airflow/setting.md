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

# 個人的な環境変数の設定 airflow.cnfでもいけるか？
echo "export AIRFLOW_HOME=/home/airflow/airflow" >> $HOME/.bashrc
echo "export AIRFLOW__CORE__LOAD_EXAMPLES=False" >> $HOME/.bashrc
echo "export AIRFLOW__SCHEDULER__CATCHUP_BY_DEFAULT=False" >> $HOME/.bashrc
```
`$HOME/yosatweets/airflow/systemd/airflow.env`の`xxxxx`部分は環境に合わせて変更が必要。
完了したら一度シェルを再起動。
```
airflow initdb
mkdir -p $HOME/airflow/dags
ln -s $HOME/yosatweets/airflow/dags $HOME/airflow/dags/yosatweets
cat $HOME/yosatweets/airflow/systemd/airflow.env >> $HOME/airflow/airflow.env
sudo ln -s $HOME/yosatweets/airflow/systemd/airflow-scheduler.service /etc/systemd/system/airflow-scheduler.service
sudo systemctl enable airflow-scheduler
sudo systemctl start airflow-scheduler
```

