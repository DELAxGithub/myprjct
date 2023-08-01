import gspread
from googletrans import Translator
from oauth2client.service_account import ServiceAccountCredentials

# Google APIにアクセスするための認証
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/delax/Documents/Projects/ieltsspeaking/client_secret.json', scope)
client = gspread.authorize(creds)

# スプレッドシートの取得
sh = client.open('Expression')
worksheet = sh.worksheet("Words")

# A列のデータを取得
values_list = worksheet.col_values(1)

# 翻訳器の作成
translator = Translator()

# A列の各単語を翻訳
for i, word in enumerate(values_list, start=1):
    translation = translator.translate(word, dest='ja')  # 英語から日本語に翻訳
    worksheet.update_cell(i, 2, translation.text)  # 翻訳結果をB列に書き込み
