import os
import openai
import gspread
import time  # 追加
from oauth2client.service_account import ServiceAccountCredentials

# Google SheetsとOpenAIの認証情報を設定します。
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/delax/Documents/Projects/ieltsspeaking/client_secret.json"

# Google Sheetsからデータを取得します。
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/delax/Documents/Projects/ieltsspeaking/client_secret.json', scope)
gc = gspread.authorize(creds)

openai.api_key = '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'

def create_answer(context, prompt, max_tokens=220, temperature=0.7):
    message = {
        "role": "system",
        "content": context
    }, {
        "role": "user",
        "content": prompt
    }

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message,
      max_tokens=max_tokens,
      temperature=temperature
    )
    
    return response['choices'][0]['message']['content']

sh = gc.open('example1')
worksheet = sh.worksheet('Part1')
rows = worksheet.get_all_records()  # Returns a list of dictionaries, by column name

# 各問題に対してループを行います。
for i, row in enumerate(rows):
    question = row['A']  # Assuming column names are 'A', 'B', 'C', etc.
    status = row['C']
    if question:  # このチェックは、セルが空でないことを確認します。
        context = f"""
        You are an IELTS teacher.
        You will be asked to think of a model response to a hypothetical question from Part 1 of the Speaking Test that would aim for an estimated score of 6.5 to 7.5.
        The student's status is {status}.If there is a shortage of information, you can imagine the rest. please write model response only.
        """
        answer = create_answer(context, question)
        # 生成した回答を質問の隣のセル（B列）に書き込みます。
        worksheet.update_cell(i+2, 2, answer)
        time.sleep(1)  # 毎回の書き込み後に1秒間の待機時間を設定します。
