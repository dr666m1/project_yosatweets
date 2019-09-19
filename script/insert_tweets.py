import common
import pandas as pd
import sqlite3
import os
try:
    os.chdir(os.path.dirname(__file__))
except:
    pass

#===== search_tweets =====
with common.make_conn("./../data/this_week.db") as conn_this,common.make_conn("./../data/last_week.db") as conn_last:
    try:
        since_id=pd.read_sql_query("select max(id) as id from tweets;",conn_this)["id"].values[0]
    except (sqlite3.OperationalError,pd.io.sql.DatabaseError) as e:
        try:
            since_id=pd.read_sql_query("select max(id) as id from tweets;",conn_last)["id"].values[0]
        except (sqlite3.OperationalError,pd.io.sql.DatabaseError) as e:
            since_id=0

data=common.search_tweets("#よさこい -filter:retweets",since_id)

if 0 < data.shape[0]:
    with common.make_conn("./../data/this_week.db") as conn:
        data.to_sql("tweets",conn,if_exists="append",index=False,dtype={"created_at":"TEXT","id":"INTEGER","text":"TEXT","user":"TEXT"})

