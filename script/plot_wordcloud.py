#!/usr/bin/env python3
import os
from janome.tokenizer import Tokenizer
#import MeCab
import common
import pandas as pd
from wordcloud import WordCloud
try:
    os.chdir(os.path.dirname(__file__))
except NameError as e:
    pass

with common.make_conn("./../data/last_week.db") as conn:
    df=pd.read_sql_query("select * from tweets;",conn)

t=Tokenizer()
word_freq={}
for txt in df["text"]:
    for token in t.tokenize(txt):
        if token.part_of_speech.split(",")[0] in ["名詞","形容詞","動詞"]:
            if token.base_form in word_freq.keys():
                word_freq[token.base_form]+=1
            else:
                word_freq[token.base_form]=1

#chasen=MeCab.Tagger("-Ochasen")
#node=chasen.parseToNode(df["text"][0])
#for txt in df["text"]:
#    node=chasen.parseToNode(txt)
#    while node is not None:
#        word=node.feature.split(",")[6]
#        if node.feature.split(",")[0] in ["名詞","形容詞","動詞"]:
#            if word in word_freq.keys():
#                word_freq[word]+=1
#            else:
#                word_freq[word]=1
#        node=node.next

wc=WordCloud(font_path="./../font/YuGothB.ttc")
wc.generate_from_frequencies(word_freq)
wc.to_file("./../plot/wordcloud.png")

