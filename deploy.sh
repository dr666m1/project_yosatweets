#!/bin/bash
cd $(dirname $0)
gcloud functions deploy yosatweets_inseart_tweets --entry-point main_insert_tweets --runtime python37 --trigger-http --memory 2048MB

gcloud functions deploy yosatweets_count_tweets --entry-point main_count_tweets --runtime python37 --trigger-http --memory 2048MB

gcloud functions deploy yosatweets_plot_line_chart --entry-point main_plot_line_chart --runtime python37 --trigger-http --memory 2048MB

gcloud functions deploy yosatweets_plot_wordcloud --entry-point main_plot_wordcloud --runtime python37 --trigger-http --memory 2048MB
