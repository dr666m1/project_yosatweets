ignore_words = [
    "いる",
    "ある",
    "くる",
    "する",
    "ない",
    "さん",
    "さま",
    "れる",
    "せる",
    "くださる",
    "なる",
    "それ",
    "ところ",
    "とき",
    "頃",
    "様",
    "者",
    "衆",
    "組",
    "人",
    "中",
    "in",
    "さ",
    "の",
    "火", "水", "木", "金", "土",
    "日", "月", "年",
    "市", "市立", "県",
    "_",
    "こと",
    "ここ",
    "もん",
    "笑",
    "　#", "　＃", "#", "＃",
    "+", "＋",
    "*",
    "-",
    ".",
    "(", ")", "()",
    "♪",
    "/",
    "~", "～",
    "w",
    "方",
    "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "１", "２", "３", "４", "５", "６", "７", "８", "９",
]

replace_words = {
    "竜馬": "龍馬",
    "オトネコ": "おとねこ",
    "国士": "國士",
    "(国|國)士(無|舞)双": "國士舞双",
    "白里浜っ子": "白里・浜っ子",
    "(え|ゑ)(え|ぇ)じゃないか祭り?": "ゑぇじゃないか祭り",
    "元気祭": "元氣祭",
    "https?://[a-zA-Z0-9/.]+": "",
    "@[a-zA-Z0-9_]+": "",
    "第[0-9０-９]+回": "",
    "[0-9０-９]日目": "",
    "よさこいエイト": "よさこい8",
}
