import nltk
import re
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def filter_english_text(input_file_name: str, output_file_name: str):
    """
    Filters out English sentences from the given text file.
    
    Args:
    input_file_name: str : The name of the input text file.
    output_file_name: str : The name of the output text file.
    """
    stop_words = set(stopwords.words('english'))
    english_text = []

    with open(input_file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        words = nltk.word_tokenize(line)
        # Remove non-alphabetic tokens and convert to lower case
        words = [word.lower() for word in words if word.isalpha()]
        if words and all(word in stop_words or re.match("[a-z]", word) for word in words):
            english_text.append(line)
        
    with open(output_file_name, 'w', encoding='utf-8') as out_file:
        out_file.writelines(english_text)

if __name__ == "__main__":
    input_file = "/Users/delax/Documents/KindlePDF/txt/essentials/essentials.txt"
    output_file = "/Users/delax/Documents/KindlePDF/txt/essentials/essentials_english.txt"
    filter_english_text(input_file, output_file)
