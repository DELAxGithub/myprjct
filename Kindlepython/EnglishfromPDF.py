
from pdfminer.high_level import extract_text

def extract_english_from_pdf(pdf_path):
    # PDFからテキストを抽出
    text = extract_text(pdf_path)

    # NLTKを用いて英語の文章のみ抽出
    import nltk
    from nltk.tokenize import sent_tokenize
    nltk.download('punkt')

    sentences = sent_tokenize(text)
    english_sentences = [sent for sent in sentences if detect_language(sent) == 'english']
    
    # 英語の文章を連結
    english_text = " ".join(english_sentences)
    
    return english_text

def detect_language(text):
    from langdetect import detect
    try:
        return detect(text)
    except:
        return None

pdf_path = "/Users/delax/Documents/KindlePDF/image/essentials_combined.pdf" # ここにPDFのパスを指定
output_text = extract_english_from_pdf(pdf_path)

with open("english_text.txt", 'w', encoding='utf-8') as f:
    f.write(output_text)
