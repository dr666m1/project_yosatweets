#!/usr/bin/env python3
import os
import pandas as pd
import common
import matplotlib.pyplot as plt
try:
    os.chdir(os.path.dirname(__file__))
except NameError as e:
    pass

#===== insert =====
with common.make_conn("./../data/last_week.db") as conn_last:
    count_df=pd.read_sql_query("select count(*) as count from tweets;",conn_last)
    count_df["date"]=(pd.Timestamp.today() + pd.tseries.offsets.Day(-7)).strftime("%Y-%m-%d")

with common.make_conn("./../data/trend.db") as conn_trend:
    count_df.to_sql("weekly",conn_trend,if_exists="append",index=False)

#===== plot =====
with common.make_conn("./../data/trend.db") as conn_trend:
    trend_df=pd.read_sql_query("select * from weekly;",conn_trend)

trend_df["date"]=pd.to_datetime(trend_df["date"])
trend_df.plot.line(x="date",y="count")
plt.savefig("./../plot/trend.png")

#===== tweet =====
common.tweet("今週の #よさこい のツイート数はxx\n先週との差分は+-xx\n\n#よさこい","./../plot/chart.png")

