## 前提
- gceのf1-micro
- osはUbuntu-18.04
- ユーザー名はairflow

## 導入
以下を実行。pythonは3.5.3以降が必須（https://github.com/pydata/xarray/issues/2866）。
```
# installまで
sudo apt update
sudo apt -y install python3.7 python3-pip zip
pip3 install --upgrade apache-airflow requests


# githubからpull
git clone https://github.com/dr666m1/project_yosatweets.git $HOME/yosatweets
```
`$HOME/yosatweets/airflow/dags/package`の下に`yosatweets_config.py`を作成
```yosatweets_config.py
sandbox_token = "xxxxx"
gcp_project = "xxxxx"
```

完了したら一度シェルを再起動。
```
airflow initdb
cp $HOME/yosatweets/airflow/airflow.cfg $HOME/airflow/airflow.cfg
mkdir -p $HOME/airflow/dags
cd $HOME/yosatweets/airflow/dags
zip -r $HOME/airflow/dags/yosatweets *
airflow scheduler -D # start as daemon
```

