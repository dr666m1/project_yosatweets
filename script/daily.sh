#!/bin/bash
cd $(dirname $0)
if [ $(date '+%w') -eq 1 ]; then
    rm ./../data/last_week.db
    mv ./../data/this_week.db ./../data/last_week.db
    $HOME/anaconda3/envs/yosatweets/bin/python3 ./count_tweets.py > ./../log/count_tweets.log 2>&1
elif [ $(date '+%w') -eq 3 ]; then
    $HOME/anaconda3/envs/yosatweets/bin/python3 ./plot_wordcloud.py > ./../log/plot_wordcloud.log 2>&1
fi

