import pdfplumber
import spacy

import os

path = "image.pdf"
print("Current directory:", os.getcwd())
print("File exists?", os.path.exists(path))


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Only add if not None
                text += page_text + "\n"
    return text.strip()


print("hello")
print(extract_text_from_pdf(path))
print("hii")
