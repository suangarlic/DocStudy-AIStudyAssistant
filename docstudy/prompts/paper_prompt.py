def build_paper_summary_prompt(text):
    return f"""你是一名资深学术论文导师。请根据以下论文内容，为研究者提供一篇5分钟就能读完的论文速读：

要求：
1. 用简洁的语言概括论文核心内容
2. 提炼研究背景和动机
3. 总结核心贡献（3-5点）
4. 给出结论和展望
5. 使用Markdown格式输出

请在Markdown分析内容之前，先输出一段结构化的JSON学习路线数据，格式如下：
```json
[
  {{"stage":"论文速读","difficulty":1,"duration":"5分钟"}}
]
```

论文内容：
{text[:8000]}"""


def build_paper_innovation_prompt(text):
    return f"""你是一名资深学术论文分析师。请深入分析以下论文的创新点：

要求：
1. 识别论文的主要创新点（3-5个）
2. 分析每个创新点的技术突破和贡献
3. 对比现有方法，指出改进之处
4. 评估创新点的学术价值和实际意义
5. 使用Markdown格式输出

请在Markdown分析内容之前，先输出一段结构化的JSON学习路线数据，格式如下：
```json
[
  {{"stage":"创新点分析","difficulty":3,"duration":"15分钟"}}
]
```

论文内容：
{text[:8000]}"""


def build_paper_tech_route_prompt(text):
    return f"""你是一名资深技术专家。请拆解以下论文的技术路线：

要求：
1. 构建完整的技术路线图
2. 分析每个技术环节的实现方法
3. 指出关键技术难点和解决方案
4. 评估技术可行性和潜在风险
5. 使用Markdown格式输出

请在Markdown分析内容之前，先输出一段结构化的JSON学习路线数据，格式如下：
```json
[
  {{"stage":"技术路线拆解","difficulty":4,"duration":"20分钟"}}
]
```

论文内容：
{text[:8000]}"""


def build_paper_reproduction_prompt(text):
    return f"""你是一名资深研究员。请为以下论文编写复现指南：

要求：
1. 列出所需的环境配置和依赖
2. 提供完整的复现步骤（可复制粘贴）
3. 给出关键代码示例和解释
4. 指出可能遇到的问题和解决方案
5. 提供评估指标和验证方法
6. 使用Markdown格式输出

请在Markdown分析内容之前，先输出一段结构化的JSON学习路线数据，格式如下：
```json
[
  {{"stage":"复现指南","difficulty":5,"duration":"30分钟"}}
]
```

论文内容：
{text[:8000]}"""