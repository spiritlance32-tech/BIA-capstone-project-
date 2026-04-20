import fitz  # PyMuPDF
import re
from pathlib import Path

def clean_text(text):
    """
    Removes non-printable characters and 'garbage' 
    common in messy PDF extractions.
    """
    # 1. Replace multiple newlines/spaces with singles
    text = re.sub(r'\s+', ' ', text)
    # 2. Keep only standard printable characters (ASCII-ish)
    # This removes the weird cyrillic/garbage icons you saw
    text = re.sub(r'[^\x20-\x7E\n]', '', text)
    return text.strip()

def clean_garbage(text):
    # 1. Strip non-printable characters
    text = "".join(char for char in text if char.isprintable())
    # 2. Remove words that look like gibberish (mixed symbols/letters)
    # This specifically targets the 'auths1hood' type junk
    words = text.split()
    clean_words = [w for w in words if not (re.search(r'[^\w\s]', w) and len(w) > 10)]
    return " ".join(clean_words)

def load_documents(folder="data/pdfs"):
    docs = []
    for file_path in Path(folder).glob("*.pdf"):
        with fitz.open(file_path) as doc:
            for page in doc:
                # Use "dict" extraction - it's much harder to fool than "text"
                # This treats the PDF as a set of spans rather than a raw string
                text_dict = page.get_text("dict")
                page_text = ""
                for block in text_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                page_text += span["text"] + " "
                
                # Force UTF-8 and strip the junk
                cleaned = clean_garbage(page_text)
                if len(cleaned) > 30:
                    docs.append(f"[Source: {file_path.name}] {cleaned}")
    return docs

