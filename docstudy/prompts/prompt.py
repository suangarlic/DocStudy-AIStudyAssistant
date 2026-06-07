def build_learning_prompt(text):
    return f"""你是一个资深技术导师。请根据以下技术文档：
1. 提取前置知识
2. 标注掌握程度（1-5星）
3. 给出学习路线（由易到难）

要求：
- 面向初学者
- 通俗易懂
- 使用Markdown输出

文档内容：
{text[:6000]}"""


def build_teaching_prompt(text):
    return f"""你是一名资深技术讲师。请用"教学方式"解释以下技术内容：要求：1. 不要总结，要讲课2. 使用类比3. 多举生活例子4. 适合零基础5. 结构清晰输出格式：- 是什么- 为什么需要它- 举个例子- 一个简单代码- 总结文档内容：{text[:6000]}"""


def build_project_prompt(text):
    return f"""你是一名资深技术导师。根据以下技术文档，为初学者只设计1个入门实践项目：
1、项目定位：聚焦该技术3~5个日常高频常用功能；
2、输出内容必须包含完整四项：
（1）项目目标：明确要学会的几个核心常用功能；
（2）详细环境配置：系统适配、Python/软件版本、全平台安装命令（Windows/macOS/Linux）、pip安装指令、镜像源配置；
（3）分步实现教程：由浅入深分步操作，每一步写清操作目的+复制即用指令；
（4）带详细注释的完整可运行代码，标注每段代码对应哪个常用功能；
3、零基础友好，所有命令复制粘贴即可运行，无省略步骤；
4、统一Markdown排版输出。

文档内容：{text[:6000]}"""


def split_text(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]


def build_rag_prompt(context, question):
    return f"""你是一个技术文档助手。请根据以下文档内容回答问题：要求：- 准确- 给出代码示例- 通俗易懂文档内容：{context}问题：{question}"""
