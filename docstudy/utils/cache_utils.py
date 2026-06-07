import os
import hashlib
import json


RESULT_CACHE_DIR = "result_cache"

if not os.path.exists(RESULT_CACHE_DIR):
    os.makedirs(RESULT_CACHE_DIR)


def get_result_cache_key(url, mode, question=""):
    key_str = f"{url}||{mode}||{question}"
    return hashlib.md5(key_str.encode('utf-8')).hexdigest()


def save_result(url, mode, question, result):
    cache_key = get_result_cache_key(url, mode, question)
    cache_file = os.path.join(RESULT_CACHE_DIR, f"{cache_key}.json")
    data = {
        "url": url,
        "mode": mode,
        "question": question,
        "result": result,
        "timestamp": os.path.getmtime(cache_file) if os.path.exists(cache_file) else None
    }
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def load_result(url, mode, question=""):
    cache_key = get_result_cache_key(url, mode, question)
    cache_file = os.path.join(RESULT_CACHE_DIR, f"{cache_key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("result", "")
    return ""