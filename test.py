import config
import user_dic
import pandas as pd
from google.cloud import bigquery
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import numpy as np
import re

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

def db2freq(start_yyyymmdd, end_yyyymmdd, dtype):
    client = bigquery.Client()
    query = """
        select *
        from `{}`
        where date(created_at) between '{}' and '{}'
    """.format(config.table_contents, start_yyyymmdd, end_yyyymmdd)
    df = client.query(query).result().to_dataframe()
    if dtype == "raw":
        return df
    elif dtype == "freq":
        t = Tokenizer("./user_dic.csv", udic_type="simpledic", udic_enc="utf8")
        cnt_df = pd.concat([text2df(x, t) for x in df["content"]]).groupby(level=0).sum()
        return cnt_df


freq = db2freq("2020-03-10", "2020-03-18", "freq")
freq.sort_values("freq", ascending=False).iloc[:50, 0]

raw = db2freq("2020-03-10", "2020-03-18", "raw")
raw.iloc[:, :20]["content"]
