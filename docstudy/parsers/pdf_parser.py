import os
import hashlib
import fitz


PDF_CACHE_DIR = "pdf_cache"

if not os.path.exists(PDF_CACHE_DIR):
    os.makedirs(PDF_CACHE_DIR)


def get_pdf_cache_key(file_name, file_content):
    key_str = f"{file_name}||{hashlib.md5(file_content).hexdigest()}"
    return hashlib.md5(key_str.encode('utf-8')).hexdigest()


def extract_text_from_pdf(file_bytes, file_name):
    cache_key = get_pdf_cache_key(file_name, file_bytes)
    cache_file = os.path.join(PDF_CACHE_DIR, f"{cache_key}.txt")
    
    if os.path.exists(cache_file):
        print(f"[PDF] Loading from cache: {cache_file}")
        with open(cache_file, 'r', encoding='utf-8') as f:
            return f.read(), ""
    
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        cleaned = "\n".join([line.strip() for line in text.split("\n") if line.strip()])
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        print(f"[PDF] Extracted {len(cleaned)} characters, cached at {cache_file}")
        return cleaned, ""
    except Exception as e:
        print(f"[PDF] Error extracting text: {e}")
        return "", str(e)