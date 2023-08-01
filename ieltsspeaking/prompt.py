import os
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# OpenAIのAPIキーを設定します。
openai.api_key = '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'

def generate_text(prompt):
    message = {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=message
    )

    return response['choices'][0]['message']['content']

# Google SheetsとOpenAIの認証情報を設定します。
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/delax/Documents/Projects/ieltsspeaking/client_secret.json"

# Google Sheetsからデータを取得します。
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/delax/Documents/Projects/ieltsspeaking/client_secret.json', scope)
gc = gspread.authorize(creds)

# Google Sheetsからプロンプトを読み込みます。
sh = gc.open('example1')
worksheet = sh.sheet1
prompts = worksheet.get_all_values()

# 別のGoogle Sheetsを開きます。
sh2 = gc.open('answer1')
worksheet2 = sh2.sheet1

# 各プロンプトに対してループを行います。
for i, row in enumerate(prompts):
    prompt = row[0]  # プロンプトは各行の最初の要素とします。

    # プロンプトを使用してテキストを生成します。
    result = generate_text(prompt)

    # 結果をGoogle Sheetsに書き込みます。
    worksheet2.update_cell(i+1, 1, result)
