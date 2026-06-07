import re
import os
import hashlib
import requests
from bs4 import BeautifulSoup


CACHE_DIR = "cache"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def get_cache_filename(url):
    md5_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, f"{md5_hash}.txt")


def validate_url(url):
    if not url or not isinstance(url, str):
        return False, "请输入URL地址"
    
    url = url.strip()
    
    if not re.match(r'^https?://', url, re.IGNORECASE):
        return False, "URL格式不正确，请以 http:// 或 https:// 开头"
    
    domain_pattern = r'^https?://[a-zA-Z0-9][a-zA-Z0-9-]*(\.[a-zA-Z0-9][a-zA-Z0-9-]*)+(/.*)?$'
    if not re.match(domain_pattern, url):
        return False, "URL格式不正确，请检查域名是否有效"
    
    return True, ""


def is_likely_document(text):
    if not text or len(text) < 200:
        return False, "网页内容过短，可能不是技术文档"
    
    text_lower = text.lower()
    
    doc_indicators = [
        "documentation", "docs", "guide", "tutorial", "api", "reference",
        "readme", "manual", "introduction", "getting started", "installation",
        "使用指南", "文档", "教程", "入门", "安装", "配置", "开发", "技术"
    ]
    
    if any(indicator in text_lower for indicator in doc_indicators):
        return True, ""
    
    if len(text) > 1000 and "github" in text_lower:
        return True, ""
    
    return False, "未识别到技术文档特征，请确保输入的是技术文档链接"


def fetch_text(url):
    cache_file = get_cache_filename(url)
    
    if os.path.exists(cache_file):
        print(f"[CACHE] Loading cached content for: {url}")
        with open(cache_file, 'r', encoding='utf-8') as f:
            clean = f.read()
        return clean, None
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        
        text = soup.get_text(separator="\n")
        clean = "\n".join([
            t.strip() for t in text.split("\n") if t.strip()
        ])
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(clean)
        print(f"[CACHE] Saved content to cache: {cache_file}")
        
        return clean, None
    
    except requests.exceptions.RequestException as e:
        return None, f"请求失败: {str(e)}"
