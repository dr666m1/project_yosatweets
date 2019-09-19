#!/bin/bash
cd $(dirname $0)
$HOME/anaconda3/envs/yosatweets/bin/python3 ./insert_tweets.py > ./../log/insert_tweets_$(date '+%H').log 2>&1
