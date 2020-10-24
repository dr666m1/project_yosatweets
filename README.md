**このbotは停止しました。今までフォローしてくださっていた方々、ありがとうございました（2020/10/24追記）**

# YosaTweets
<img src="https://user-images.githubusercontent.com/26474260/76974627-c591a200-6974-11ea-95c0-edc3dd7a40a5.jpg" width="300px">

## コンセプト
`よさこい`を含むツイートの分析を定期的に実行するアカウントです（`@TweetsYosa`）。

踊り子の皆さん、フォロー＆RTよろしくお願いします！

## 分析内容
### ツイート数の分析
<img src="https://user-images.githubusercontent.com/26474260/76974158-33899980-6974-11ea-8b59-bb8292bbf5ff.png" width="300px">

毎週月曜日に公開。

前の週の月～日曜日の`よさこい`を含むツイート数です。

### ツイート内容の分析
<img src="https://user-images.githubusercontent.com/26474260/76974163-34bac680-6974-11ea-9f51-39ffd23acd70.png" width="300px">

毎週水曜日に公開。

前の週の月～日曜日の`よさこい`を含むツイートから話題（というか名詞）を抽出し、ワードクラウドにしています。

出現回数が多い名詞は大きく、少ない名詞は小さく表示されます。

## Q and A
### ほかの分析はしないの？
検討中です。直近で考えているのはYouTubeのデータを分析した演舞動画の紹介とか。

何かアイディアあればTwitterとかで連絡いただければ。

### ワードクラウドの固有名詞が途中で切れている...
なるべくチーム名やイベント名も辞書登録したいのですが、間に合っていません。

`user_dic.csv`で整理しているので、よければプルリクエストしていただけると嬉しいです。

形式は[Janomeの簡易辞書フォーマット](https://mocobeta.github.io/janome/#v0-2-7)です。

### どうやって実装してるの？
基本的に[GCP](https://cloud.google.com/?hl=ja)の無料枠で動いています。具体的には以下。

- CloudFunctions
- BigQuery
- CloudStorage
- ComputeEngine (Apache Airflow)

TwitterのAPIはpremium search apiではなくstandard search apiを叩いているので、若干漏れ取得漏れがあるかもしれません。
コードは自由にコピペしてください。特に連絡は不要ですが、Twitterで声をかけてもらえると喜びます。
