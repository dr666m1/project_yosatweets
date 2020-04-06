from requests_oauthlib import OAuth1Session
import config
import user_dic
import json
import pandas as pd
import datetime
from google.cloud import bigquery
from google.cloud import storage
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
import io
from wordcloud import WordCloud
import numpy as np
import re
import tempfile
import altair as alt

#===== common =====
class MyException(Exception):
    pass

def make_sess():
    ck=config.CONSUMER_KEY
    cs=config.CONSUMER_SECCRET
    at=config.ACCESS_TOKEN
    ats=config.ACCESS_TOKEN_SECRET
    sess=OAuth1Session(ck, cs, at, ats)
    return sess

def post_tweet(text, img=None):
    sess = make_sess()
    params = {"status": text}
    if img is not None:
        url = "https://upload.twitter.com/1.1/media/upload.json"
        files = {"media": img}
        res = sess.post(url, files=files)
        media_id = json.loads(res.text)["media_id"]
        params["media_ids"] = media_id
    url = "https://api.twitter.com/1.1/statuses/update.json"
    sess.post(url, params=params)

#===== insert tweets =====
url_search = "https://api.twitter.com/1.1/search/tweets.json"
def search_tweets(query,since_id=0):
    params = {
        "q": query,
        "count": 100,
        "result_type": "recent",
        "since_id": since_id
    }
    sess = make_sess()
    res = sess.get(url_search, params=params)
    data_json = json.loads(res.text)
    n = len(data_json["statuses"])
    if n == 0:
        raise MyException("no tweets")
    data_df = pd.DataFrame({
        "created_at": [data_json["statuses"][i]["created_at"] for i in range(n)],
        "id": [data_json["statuses"][i]["id"] for i in range(n)],
        "content": [data_json["statuses"][i]["text"] for i in range(n)],
        "user": [data_json["statuses"][i]["user"]["screen_name"] for i in range(n)]
    })
    data_df["created_at"] = pd.to_datetime(data_df["created_at"])
    return data_df

def insert_tweets(hash_tag):
    client = bigquery.Client()
    # search latest tweets
    query = "select max(id) from `{}`".format(config.table_contents)
    latest_id = client.query(query).result().to_dataframe().iloc[0, 0]
    if latest_id is None: latest_id = 0
    # insert to bq
    try:
        df = search_tweets(hash_tag, latest_id)
        table = client.get_table(config.table_contents)
        job = client.load_table_from_dataframe(df, config.table_contents)
        job.result()
    except MyException as e:
        print(e)

def main_insert_tweets(request):
    insert_tweets("#よさこい -filter:retweets")

#===== count tweets =====
def count_tweets(today=datetime.datetime.now()):
    client = bigquery.Client()
    start_yyyymmdd = (today - datetime.timedelta(days=today.weekday() + 7)).strftime("%Y-%m-%d")
    end_yyyymmdd = (today - datetime.timedelta(days=today.weekday() + 1)).strftime("%Y-%m-%d")
    query = """
        select count(distinct id)
        from `{}`
        where date(created_at) between '{}' and '{}'
    """.format(config.table_contents, start_yyyymmdd, end_yyyymmdd)
    res_count = client.query(query).result().to_dataframe().iloc[0, 0]
    job = client.load_table_from_json(
        [{"created_at": start_yyyymmdd, "n": int(res_count)}],
        config.table_counts
    )
    job.result()

def main_count_tweets(request):
    count_tweets()

#===== plot line chart =====
def plot_line_chart():
    # extract data
    client_bq = bigquery.Client()
    client_gcs = storage.Client()
    query = """
        select *
        from `{}`
    """.format(config.table_counts)
    df_all = client_bq.query(query).result().to_dataframe()
    df_recent = df_all.sort_values("created_at", ascending=False).iloc[:50, :]
    # plot (all)
    bucket = client_gcs.get_bucket("dr666m1_yosatweets")
    blob = bucket.blob("plot_line_chart.html")
    df_all["created_at"] = pd.to_datetime(df_all["created_at"])
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = tmp_dir + "/plot_line_chart.html"
        chart = alt.Chart(df_all).mark_line().encode(
            x="created_at",
            y="n",
            tooltip=["created_at", "n"]
        ).interactive().save(tmp_file)
        blob.upload_from_filename(filename=tmp_file)
        blob.make_public()
        url = blob.public_url
    # prepare message
    cnt = df_recent.iloc[0, 1]
    diff = cnt - df_recent.iloc[1, 1]
    msg = "【定期】\n先週の #よさこい のツイート数：{:,d}\n前週比増減：{:+,d}\n{}".format(cnt, diff, url)
    # plot (recent)
    df_recent.plot.line(x="created_at", y="n")
    # tweets
    with io.BytesIO() as img:
        plt.savefig(img, format="png")
        post_tweet(text=msg, img=img.getvalue())

def main_plot_line_chart(request):
    plot_line_chart()

#===== plot wordcloud =====
def text2df(content, t):
    content_tmp = content
    for i, j in user_dic.replace_words.items():
        content_tmp = re.sub(i, j, content_tmp)
    words = [
        x.base_form for x in t.tokenize(content_tmp)
        if (x.base_form not in user_dic.ignore_words and x.part_of_speech.split(",")[0] == "名詞")
    ]
    keys, freqs = np.unique(words, return_counts=True)
    return pd.DataFrame({"freq": freqs}, index=keys)

def plot_wordcloud(today=datetime.datetime.now()):
    client = bigquery.Client()
    start_yyyymmdd = (today - datetime.timedelta(days=today.weekday() + 7)).strftime("%Y-%m-%d")
    end_yyyymmdd = (today - datetime.timedelta(days=today.weekday() + 1)).strftime("%Y-%m-%d")
    query = """
        select *
        from `{}`
        where date(created_at) between '{}' and '{}'
    """.format(config.table_contents, start_yyyymmdd, end_yyyymmdd)
    df = client.query(query).result().to_dataframe()
    t = Tokenizer("./user_dic.csv", udic_type="simpledic", udic_enc="utf8")
    cnt_df = pd.concat([text2df(x, t) for x in df["content"]]).groupby(level=0).sum()
    cnt_dic = {x[0]: x[1] for x in cnt_df.itertuples()}
    wc = WordCloud(font_path="./meiryo.ttc",width=1200,height=800,colormap="Accent")
    #colormap... https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
    wc.generate_from_frequencies(cnt_dic)
    msg = "【定期】\n先週の話題 #よさこい"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = tmp_dir + "/tmp.png"
        wc.to_file(tmp_file)
        with open(tmp_file, "rb") as img:
            post_tweet(text=msg, img=img)

def main_plot_wordcloud(request):
    plot_wordcloud()

