# 📄 文件1：Day1_MVP_核心闭环.md

# 📚 DocStudy - Day1 MVP（必须完成）目标：实现最小可运行系统（核心闭环）=================================================# 🎯 项目核心目标输入一个技术文档URL：→ 输出：1. 前置知识分析2. 学习路线3. 难度评估=================================================# 🧱 一、项目结构

docstudy/  
├── app.py  
├── parser.py  
├── agent.py  
├── prompt.py  
├── .env

=================================================
# 🖥️ 二、前端（Streamlit）
## app.py
```python
import streamlit as stst.title("📚 DocStudy - AI技术文档学习助手")url = st.text_input("请输入技术文档URL")mode = st.selectbox(    "选择功能",    [        "学习路线分析",        "入门讲解",        "项目生成",        "开发者问答"    ])btn = st.button("开始分析")if btn:    st.write("处理中...")
```
---

## 运行方式
streamlit run app.py
```

=================================================

# 🌐 三、文档解析模块 parser.py

```
import requestsfrom bs4 import BeautifulSoupdef fetch_text(url):    headers = {"User-Agent": "Mozilla/5.0"}    res = requests.get(url, headers=headers, timeout=10)    soup = BeautifulSoup(res.text, "html.parser")    for tag in soup(["script", "style"]):        tag.decompose()    text = soup.get_text(separator="\n")    clean = "\n".join([        t.strip() for t in text.split("\n") if t.strip()    ])    return clean
```

=================================================

# 🤖 四、LLM调用 agent.py（DeepSeek）

```
import osimport requestsfrom dotenv import load_dotenvload_dotenv()API_KEY = os.getenv("DEEPSEEK_API_KEY")def call_llm(prompt):    url = "https://api.deepseek.com/chat/completions"    headers = {        "Authorization": f"Bearer {API_KEY}",        "Content-Type": "application/json"    }    data = {        "model": "deepseek-chat",        "messages": [            {"role": "user", "content": prompt}        ],        "temperature": 0.3    }    res = requests.post(url, json=data, headers=headers)    return res.json()["choices"][0]["message"]["content"]
```

=================================================

# 🧠 五、Prompt设计 prompt.py

```
def build_learning_prompt(text):    return f"""你是一个资深技术导师。请根据以下技术文档：1. 提取前置知识2. 标注掌握程度（1-5星）3. 给出学习路线（由易到难）要求：- 面向初学者- 通俗易懂- 使用Markdown输出文档内容：{text[:6000]}"""
```

=================================================

# 🔗 六、主逻辑 app.py（完整版）

```
from parser import fetch_textfrom agent import call_llmfrom prompt import build_learning_promptimport streamlit as stst.title("📚 DocStudy - AI技术文档学习助手")url = st.text_input("请输入技术文档URL")mode = st.selectbox(    "选择功能",    [        "学习路线分析",        "入门讲解",        "项目生成",        "开发者问答"    ])btn = st.button("开始分析")if btn and url:    text = fetch_text(url)    prompt = build_learning_prompt(text)    result = call_llm(prompt)    st.markdown(result)
```

=================================================

# 🚀 Day1完成标准

✔ 能输入URL  
✔ 能抓取网页内容  
✔ 能调用DeepSeek  
✔ 能输出学习路线分析

=================================================

# ⚠️ Day1禁止做

❌ RAG  
❌ 视频生成  
❌ AI生图  
❌ Vue前端  
❌ Agent框架

=================================================

# 🎯 核心原则

先跑通：

URL → 文档 → LLM → 输出