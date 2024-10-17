# takasumiAPI pythonラッパー
docstringはnumpyを使用  
上の方の関数は気にしないでね

### クラス
- user ユーザー
  - .id | ID
  - .user | データ
  - money() | 所持しているものを取得
  - rank() | 順位を取得
  - is_mute() | ミュートされてるかどうか
  - history() | historyを取得
- guild ギルド（サーバー）
  - .id | ID
  - fetch() | 情報を取得
- gift ギフト
  - .id | ID
  - .data | データ

### 関数
- count()
- trade()
- server()
- status()  
はそれぞれapiそのまま
- trade_get(time) | その時間のtradeを調べる  なかったらNoneを返す
