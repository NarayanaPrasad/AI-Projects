import re
import pandas as pd
import pdfplumber
import docx

def clean_text(text):
    if not isinstance(text, str): return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_resumes_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    df['cleaned_text'] = df['Text'].apply(clean_text)
    return df[df['cleaned_text'].str.len() > 50].reset_index(drop=True)

def load_single_resume(file_path):
    """Returns (raw_text, cleaned_text) for PDF or DOCX"""
    raw_text = ""
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            raw_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        raw_text = "\n".join([p.text for p in doc.paragraphs])
    
    if not raw_text.strip():
        return "Empty Resume", ""
        
    return raw_text, clean_text(raw_text)
