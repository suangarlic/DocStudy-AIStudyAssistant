# 🚀 Day2：功能扩展（在Day1跑通基础上）

## 🎯 Day2目标（非常重要）

把你的系统从：

> “只能分析文档”

升级为：

> “能生成学习内容 + 能回答问题”

最终增加三块能力：

---

# 🧩 模块1：项目生成（核心加分功能）

## 🎯 功能

输入文档 → 自动生成：

- 入门项目

---

## 🧠 Prompt直接用这个

```
你是一名资深技术导师。根据以下技术文档，为初学者设计1个练手学习项目：要求：1. 简单易上手2. 每个项目包含：   - 项目目标   - 实现步骤   - 核心代码示例3. 必须可以实际运行4. 使用Markdown格式输出文档内容：{text}
```

---

## 🔌 接入方式（你只需要做一件事）

在 app.py 加一个分支：

```python
if mode == "实践项目练手":    text = fetch_text(url)    prompt = build_project_prompt(text)    result = call_llm(prompt)    st.markdown(result)
```

---

# 💬 模块2：开发者问答（简化RAG版）

## 🎯 功能

用户可以问：

- “这个API怎么用？”
- “Scapy sniff参数是什么？”
- “LangChain Retriever怎么写？”

---

## ⚡ 不用向量库（先简化）

直接用：

```
text → 切片 → 取前3段
```

---

## 🧠 切分函数

```
def split_text(text, size=500):    return [text[i:i+size] for i in range(0, len(text), size)]
```

---

## 🧠 RAG Prompt

```
你是一个技术文档助手。请根据以下文档内容回答问题：要求：- 准确- 给出代码示例- 通俗易懂文档内容：{context}问题：{question}
```

---

## 🔌 app.py 接入

```python
question = st.text_input("请输入问题")if mode == "开发者问答":    text = fetch_text(url)    chunks = split_text(text)    context = "\n".join(chunks[:3])    prompt = build_rag_prompt(context, question)    result = call_llm(prompt)    st.markdown(result)
```

---

# 📘 模块3：入门讲解增强（优化体验）

## 🎯 目标

把“总结”变成“老师讲课风格”

---

## 🧠 Prompt（直接替换Day1的）

```
你是一名资深技术讲师。请用“教学方式”解释以下技术内容：要求：1. 不要总结，要讲课2. 使用类比3. 多举生活例子4. 适合零基础5. 结构清晰输出格式：- 什么是什么- 为什么需要它- 举个例子- 一个简单代码- 总结文档内容：{text}
```

---

# 🔥 Day2完成后你会得到什么？

你的系统会变成：

---

## 🧠 学习能力

✔ 自动生成学习路线  
✔ 自动生成难度分析

---

## 🛠 实践能力

✔ 自动生成1个入门项目

---

## 💬 问答能力

✔ 能回答“文档相关开发问题”

---

# ⚠️ Day2关键原则（很重要）

## ❌ 不要做

- FAISS
- embedding
- agent框架
- Vue前端
- 视频生成
- AI生图

---

## ✅ 必须做

- Streamlit交互
- 3个功能分支
- LLM调用统一封装
- 文档解析复用Day1