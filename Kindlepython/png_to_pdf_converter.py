import os
import re
from PIL import Image
import img2pdf

folder_path = "/Users/delax/Documents/KindlePDF/image/essentials"

# PNG画像のリストを作成します。
png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# ファイル名内の番号に基づいてソートします。
png_files = sorted(png_files, key=lambda f: int(re.findall(r'\d+', f)[0]))

# PNG画像を開き、RGBに変換します。
imgs = [Image.open(os.path.join(folder_path, f)).convert('RGB') for f in png_files]

# フォルダ名をPDFのファイル名として使用します。
folder_name = os.path.basename(folder_path.rstrip('/'))
pdf_filename = f"{folder_name}_combined.pdf"

# PDFファイルのフルパスを定義します。
pdf_path = os.path.join(os.path.dirname(folder_path), pdf_filename)

# すべての画像を一つのPDFに変換します。
with open(pdf_path, "wb") as f:
    f.write(img2pdf.convert([os.path.join(folder_path, f) for f in png_files]))
