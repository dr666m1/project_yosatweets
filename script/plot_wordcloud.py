#!/usr/bin/env python3
import os
#from janome.tokenizer import Tokenizer
import MeCab
import common
import pandas as pd
from wordcloud import WordCloud
try:
    os.chdir(os.path.dirname(__file__))
except NameError as e:
    pass

with common.make_conn("./../data/last_week.db") as conn:
    df=pd.read_sql_query("select * from tweets;",conn)

#word_freq={}
#ignore_words=common.read_ignore_dic()
#t=Tokenizer("./../dic/user_dic.csv",udic_type="simpledic",udic_enc="utf8")
#for txt in df["text"]:
#    converted_txt=common.apply_convert_dic(txt)
#    for token in t.tokenize(converted_txt):
#        if token.base_form in ignore_words:
#            continue
#        elif token.part_of_speech.split(",")[0] in ["名詞","形容詞","動詞"]:
#            if token.base_form in word_freq.keys():
#                word_freq[token.base_form]+=1
#            else:
#                word_freq[token.base_form]=1

word_freq={}
ignore_words=common.read_ignore_dic()
chasen=MeCab.Tagger("-Ochasen -u ./../dic/user_dic.dic")
for txt in df["text"]:
    converted_txt=common.apply_convert_dic(txt)
    node=chasen.parseToNode(converted_txt)
    while node is not None:
        word=node.feature.split(",")[6]
        if word in ignore_words:
            pass
        elif node.feature.split(",")[0] not in ["名詞","形容詞","動詞"]:
            pass
        elif word in word_freq.keys():
            word_freq[word]+=1
        else:
            word_freq[word]=1
        node=node.next

wc=WordCloud(font_path="./../font/YuGothB.ttc",width=1200,height=800)
wc.generate_from_frequencies(word_freq)
wc.to_file("./../plot/wordcloud.png")

common.tweet("【定期】先週の話題\n\n#よさこい","./../plot/wordcloud.png")
