## 前提
- gceのf1-micro
- osはUbuntu-18.04
- ユーザー名はairflow

## 導入
以下を実行。pythonは3.5.3以降が必須らしい（https://github.com/pydata/xarray/issues/2866）。
```
sudo apt update
sudo apt -y install python3.7 python3-pip
pip3 install --upgrade apache-airflow requests
git clone https://github.com/dr666m1/project_yosatweets.git $HOME/yosatweets
```
シェルを再起動して以下を実行。

```
airflow initdb
cp $HOME/yosatweets/airflow/dags/* $HOME/airflow/dags
airflow unpause yosatweets_hourly_version-x.x
airflow unpause yosatweets_monday_version-x.x
airflow unpause yosatweets_wednesday_version-x.x
airflow scheduler # systemd? nohup?
```

## memo
- 環境変数はファイルで設定したい
echo "export AIRFLOW_HOME=$HOME/airflow" >> $HOME/.bashrc
echo "export AIRFLOW__CORE__LOAD_EXAMPLES=False" >> $HOME/.bashrc
echo "export AIRFLOW__SCHEDULER__CATCHUP_BY_DEFAULT=False" >> $HOME/.bashrc
echo "export SANDBOX_TOKEN=xxxxxxxxxx" >> $HOME/.bashrc
echo "export GCP_PROJECT=xxxxxxxxxx" >> $HOME/.bashrc
echo "export PYTHONPATH=$HOME/yosatweets/airflow/yosatweets" >> $HOME/.bashrc
