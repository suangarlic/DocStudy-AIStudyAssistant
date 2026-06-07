import os
import requests
import time
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")


def call_llm(prompt):
    print("=" * 60)
    print("[DEBUG] API Key loaded:", "sk-" + "*" * 20 + API_KEY[-4:] if API_KEY else "NOT FOUND")
    print("[DEBUG] Model: deepseek-v4-flash")
    print("[DEBUG] Prompt length:", len(prompt), "characters")
    print("[DEBUG] Sending request to DeepSeek API...")
    
    start_time = time.time()
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-v4-flash",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        res = requests.post(url, json=data, headers=headers, timeout=60)
        elapsed_time = time.time() - start_time
        
        print("[DEBUG] Response received in", f"{elapsed_time:.2f}", "seconds")
        print("[DEBUG] Status code:", res.status_code)
        
        if res.status_code == 200:
            response_json = res.json()
            print("[DEBUG] Response structure:", list(response_json.keys()))
            content = response_json["choices"][0]["message"]["content"]
            print("[DEBUG] Result length:", len(content), "characters")
            print("[DEBUG] Request successful!")
            print("=" * 60)
            return content
        else:
            print("[ERROR] API request failed with status", res.status_code)
            print("[ERROR] Response:", res.text[:500])
            print("=" * 60)
            raise Exception(f"API request failed: {res.status_code}")
    
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out after 60 seconds")
        print("=" * 60)
        raise
    except requests.exceptions.ConnectionError as e:
        print("[ERROR] Connection error:", str(e))
        print("=" * 60)
        raise
    except Exception as e:
        print("[ERROR] Unexpected error:", str(e))
        print("=" * 60)
        raise
