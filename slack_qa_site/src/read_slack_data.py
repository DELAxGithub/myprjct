import sqlite3

# SQLiteデータベースに接続
conn = sqlite3.connect('slack.db')
cursor = conn.cursor()

# メッセージテーブルからデータを取得
cursor.execute("SELECT user, text FROM messages")
messages = cursor.fetchall()

# コネクションを閉じる
cursor.close()
conn.close()
