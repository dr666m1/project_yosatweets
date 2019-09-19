from requests_oauthlib import OAuth1Session
import config
import contextlib
import sqlite3
import json
import pandas as pd
import re

#===== session =====
def make_sess():
    ck=config.CONSUMER_KEY
    cs=config.CONSUMER_SECCRET
    at=config.ACCESS_TOKEN
    ats=config.ACCESS_TOKEN_SECRET
    sess=OAuth1Session(ck,cs,at,ats)
    return sess

#===== database =====
def make_conn(path):
    conn=contextlib.closing(sqlite3.connect(path))
    return conn

#===== search =====
def search_tweets(query,since_id):
    params={
        "q":query,
        "count":100,
        "result_type":"recent",
        "since_id":since_id
    }
    sess=make_sess()
    url="https://api.twitter.com/1.1/search/tweets.json"
    res=sess.get(url,params=params)
    data_json=json.loads(res.text)
    n=len(data_json["statuses"])
    if n==100:
        pass
        #そのうち警告が出るようにしたい
    data_df=pd.DataFrame({
        "created_at":[data_json["statuses"][i]["created_at"] for i in range(n)],
        "id":[data_json["statuses"][i]["id"] for i in range(n)],
        "text":[data_json["statuses"][i]["text"] for i in range(n)],
        "user":[data_json["statuses"][i]["user"]["screen_name"] for i in range(n)]
    })
    data_df["created_at"]=pd.to_datetime(data_df["created_at"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    #data_df["created_at"]=(pd.to_datetime(data_df["created_at"]) + pd.offsets.Hour(9)).dt.strftime("%Y-%m-%d %H:%M:%S")
    return data_df

#===== dictionary =====
def apply_convert_dic(text):
    with open("./../dic/convert_dic.json","r") as file:
        dic=json.load(file)
    for f,t in dic["replace"].items():
        text=text.replace(f,t)
    for f,t in dic["reg-replace"].items():
        text=re.sub(f,t,text)
    return text

def read_ignore_dic():
    with open("./../dic/ignore_dic.json","r") as file:
        dic=json.load(file)["ignore_words"]
    return dic

#===== tweet =====
def tweet(text,img=None):
    sess=make_sess()
    if img is not None:
        file=open(img,"rb")
        url="https://upload.twitter.com/1.1/media/upload.json"
        files={
            "media":file
        }
        res=sess.post(url,files=files)
        media_id=json.loads(res.text)["media_id"]
        params={
            "status":text,
            "media_ids":media_id,
        }
    else:
        params={
            "status":text,
        }
    url="https://api.twitter.com/1.1/statuses/update.json"
    sess.post(url,params=params)

