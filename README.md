# 実装
## GoogleComputeEngine
無料枠のf1-microでもどうにか動く。当初Janomeを使うとMemoryErrorを吐いたためMeCabに切り替えた。
特別な権限の設定などは不要。

## mecabのインストール
mecab-python3のインストールだけでも動くが、辞書のコンパイルなどができなかったため別途DLした。
```
sudo apt install mecab libmecab-dev mecab-ipadic-utf8
```

## 辞書の整理
デフォルトのipadicを使っているが、別途自分で2種類の辞書を整備している。

### dic/convert_dic.json
表記ゆれの修正と、htmlなど不要な部分の除外に使っている。
形態素解析前に適用される。

### dict/ignore_dic.json
ワードクラウドに表示しない単語一覧。形態素解析後に適用される。

## crontabへの追記
メモリ不足をさけるため、ツイートの検索と自動投稿はタイミングをずらしている。
```
 5  0  *  *  * /bin/bash $HOME/yosatweets/script/daily.sh
 0  *  *  *  * /bin/bash $HOME/yosatweets/script/hourly.sh
```
