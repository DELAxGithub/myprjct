import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Google Sheets APIの認証情報を設定
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '/Users/delax/Documents/Projects/ieltsspeaking/client_secret.json', scope)
gc = gspread.authorize(credentials)

# Googleスプレッドシートを開く
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/19T35SDpQAr0SzblPeLzlJs06Xr0O6AeRGKtH_xs8lTI/edit#gid=1401371155')  # スプレッドシートのURLを指定
worksheet = spreadsheet.get_worksheet(0)  # 最初のワークシートを取得

# データを取得し、pandasのDataFrameに変換
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

# データのクリーニング
# ここでは、全ての列で数値以外の値をNaNに置換しています
df = df.apply(pd.to_numeric, errors='coerce')

# クリーニング後のデータを表示
print(df)
