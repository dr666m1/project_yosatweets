#!/usr/bin/env python3
import os
import pandas as pd
import common
import matplotlib.pyplot as plt
import sqlite3
try:
    os.chdir(os.path.dirname(__file__))
except NameError as e:
    pass

#===== insert =====
with common.make_conn("./../data/last_week.db") as conn_last:
    try:
        count_df=pd.read_sql_query("select count(*) as count from tweets;",conn_last)
        count_df["date"]=(pd.Timestamp.today() + pd.tseries.offsets.Day(-7)).strftime("%Y-%m-%d")
    except (sqlite3.OperationalError,pd.io.sql.DatabaseError) as e:
        count_df=pd.DataFrame({
            "count":[0],
            "date":[(pd.Timestamp.today() + pd.tseries.offsets.Day(-7)).strftime("%Y-%m-%d")],
        })

with common.make_conn("./../data/trend.db") as conn_trend:
    count_df.to_sql("weekly",conn_trend,if_exists="append",index=False)

#===== plot =====
with common.make_conn("./../data/trend.db") as conn_trend:
    trend_df=pd.read_sql_query("select * from weekly;",conn_trend)

trend_df["date"]=pd.to_datetime(trend_df["date"])
trend_df.plot.line(x="date",y="count")
plt.savefig("./../plot/trend.png")

latest2=trend_df.sort_values(by=["date"],ascending=False).tail(2)["count"].values
cnt=latest2[-1]
try:
    diff=latest2[-1]-latest2[-2]
except IndexError as e:
    diff=0

#===== tweet =====
common.tweet("【定期】\n先週の #よさこい のツイート数：{:,d}\n前週比増減：{:+,d}\n\n#よさこい".format(cnt,diff),"./../plot/trend.png")

