# DB Architecture
This database used SQLite3

.csv files are output of db.

![SQLiteアイコン](./images/sqlite_icon.svg)


## ER図
![ER図](./images/data_ER.svg)<img src="./images/data_ER.svg">


## Description
- fishery_data
PK: 場所, 日付, 漁業種類, 魚種

| カラム名 |    説明 | 例  |
| ---- | ---- | --- |
| 場所   | 船の所属湾 |     |
| 日付   | 漁の日付 |     |
| 漁業種類 | 漁業手法 |     |
| 隻数   | 漁に行った隻数 |     |
| 魚種   | 魚種 |     |
| 規格   |  |     |
| 本数   | text |     |
| 水揚量  | text |     |
| 高値   | text |     |
| 平均値  | text |     |
| 安値   | text |     |


- suion_data
PK: 場所, 日付

# データソース
[いわて大漁ナビ 岩手県水産情報配信システム](https://www.suigi.pref.iwate.jp)  
岩手県水産技術センター水産情報配信システム調べ