import os
from google.cloud import texttospeech
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google SheetsとGoogle Text-to-Speechの認証情報を設定します。
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/delax/Documents/Projects/ieltsspeaking/client_secret.json"

# Google Sheetsからデータを取得します。
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/delax/Documents/Projects/ieltsspeaking/client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Speaking_1").sheet1
data = sheet.get_all_values()

# Text-to-Speechクライアントを初期化します。
tts_client = texttospeech.TextToSpeechClient()

# 音声の設定を行います。
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# 音声の出力形式を設定します。
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Google Sheetsの各行に対してテキストから音声を生成します。
for i, row in enumerate(data):
    text = row[0]  # テキストは各行の最初の要素とします。

      # ピリオドの後のポーズを調整
    text_ssml = "<speak>" + text.replace(".", ".<break time=\"800ms\"/>") + "</speak>"

    # テキストから音声を生成します。
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 音声ファイルを保存します。
    filename = f"output_{i}.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{filename}"')
