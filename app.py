import streamlit as st
from docstudy.utils.cache_utils import load_result, save_result
from docstudy.executors.executors import execute_learning, execute_teaching, execute_project, execute_qa
from docstudy.ui.knowledge_graph import generate_knowledge_graph, clean_markdown_text
from docstudy.executors.paper_executor import (
    execute_paper_summary,
    execute_paper_innovation,
    execute_paper_tech_route,
    execute_paper_reproduction
)
from docstudy.ui.study_profile import render_sidebar


SESSION_KEYS = {
    "学习路线分析": ("res_learn", "last_url_learn"),
    "入门讲解": ("res_teach", "last_url_teach"),
    "实践项目练手": ("res_project", "last_url_project"),
    "开发者问答": ("res_qa", "last_url_qa"),
    "论文速读": ("res_paper_summary", "last_paper_name"),
    "创新点分析": ("res_paper_innovation", "last_paper_name"),
    "技术路线拆解": ("res_paper_tech", "last_paper_name"),
    "复现指南": ("res_paper_reprod", "last_paper_name"),
}


def init_session():
    defaults = {
        "res_learn": "", "res_teach": "", "res_project": "", "res_qa": "",
        "res_paper_summary": "", "res_paper_innovation": "",
        "res_paper_tech": "", "res_paper_reprod": "",
        "last_question": "",
        "stop_analysis": False,
        "last_url_learn": "", "last_url_teach": "", "last_url_project": "", "last_url_qa": "",
        "last_paper_name": "",
        "selected_learning_mode": "技术文档学习",
        "selected_mode": "学习路线分析",
        "selected_url": "",
        "selected_paper_name": "",
    }
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def render_ui():
    st.title("📚 DocStudy - AI学习助手")
    
    default_learning_mode = st.session_state.get("selected_learning_mode", "技术文档学习")
    learning_mode = st.selectbox(
        "选择学习对象",
        ["技术文档学习", "论文学习"],
        index=0 if default_learning_mode == "技术文档学习" else 1
    )
    
    if learning_mode == "技术文档学习":
        default_url = st.session_state.get("selected_url", "")
        url = st.text_input("请输入技术文档URL", value=default_url)
        
        default_mode = st.session_state.get("selected_mode", "学习路线分析")
        mode_options = ["学习路线分析", "入门讲解", "实践项目练手", "开发者问答"]
        mode_index = mode_options.index(default_mode) if default_mode in mode_options else 0
        mode = st.selectbox(
            "选择功能",
            mode_options,
            index=mode_index
        )
        
        question = st.text_input("请输入问题", value=st.session_state.last_question) if mode == "开发者问答" else None
        paper_file = None
        
    else:
        url = ""
        question = None
        
        paper_file = st.file_uploader("上传论文PDF文件", type="pdf")
        
        default_mode = st.session_state.get("selected_mode", "论文速读")
        mode_options = ["论文速读", "创新点分析", "技术路线拆解", "复现指南"]
        mode_index = mode_options.index(default_mode) if default_mode in mode_options else 0
        mode = st.selectbox(
            "选择功能",
            mode_options,
            index=mode_index
        )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        btn = st.button("开始分析")
    with col2:
        stop_btn = st.button("停止分析")
        if stop_btn:
            st.session_state.stop_analysis = True
            print("[APP] Stop analysis requested")
    
    return url, mode, question, btn, learning_mode, paper_file


def handle_document_analysis(url, mode, question, btn):
    res_key, url_key = SESSION_KEYS[mode]
    
    if btn and url:
        st.session_state.stop_analysis = False
        
        cached_result = load_result(url, mode, question or "")
        if cached_result and st.session_state[url_key] == url:
            print(f"[APP] Result already cached for {mode}, skipping LLM call")
            st.info("ℹ️ 结果已缓存，直接展示上次分析结果")
            st.session_state[res_key] = cached_result
        else:
            if mode == "学习路线分析":
                result = execute_learning(url)
            elif mode == "入门讲解":
                result = execute_teaching(url)
            elif mode == "实践项目练手":
                result = execute_project(url)
            elif mode == "开发者问答":
                result = execute_qa(url, question)
            
            if result:
                st.session_state[res_key] = result
                st.session_state[url_key] = url
                save_result(url, mode, question or "", result)
    
    current_result = st.session_state.get(res_key, "")
    current_url = st.session_state.get(url_key, "")

    if current_result and current_url == url:
        if mode == "学习路线分析":
            st.subheader("📚 学习路线")
            generate_knowledge_graph(current_result)
            st.subheader("📋 详细分析")
            st.markdown(clean_markdown_text(current_result))
        else:
            st.markdown(current_result)
    elif url:
        cached_result = load_result(url, mode, question or "")
        if cached_result:
            st.session_state[res_key] = cached_result
            st.session_state[url_key] = url
            if mode == "学习路线分析":
                st.subheader("📚 学习路线")
                generate_knowledge_graph(cached_result)
                st.subheader("📋 详细分析")
                st.markdown(clean_markdown_text(cached_result))
            else:
                st.markdown(cached_result)
            st.info("ℹ️ 从本地缓存加载上次分析结果")


def handle_paper_analysis(paper_file, mode, btn):
    res_key, name_key = SESSION_KEYS[mode]
    
    if btn and paper_file:
        st.session_state.stop_analysis = False
        
        file_name = paper_file.name
        file_bytes = paper_file.read()
        paper_file.seek(0)
        
        cache_key = f"paper_{file_name}_{hash(file_bytes)}"
        cached_result = load_result(cache_key, mode, "")
        
        if cached_result:
            print(f"[APP] Result already cached for {mode}, skipping LLM call")
            st.info("ℹ️ 结果已缓存，直接展示上次分析结果")
            st.session_state[res_key] = cached_result
            st.session_state[name_key] = file_name
        else:
            if mode == "论文速读":
                result = execute_paper_summary(file_bytes, file_name)
            elif mode == "创新点分析":
                result = execute_paper_innovation(file_bytes, file_name)
            elif mode == "技术路线拆解":
                result = execute_paper_tech_route(file_bytes, file_name)
            elif mode == "复现指南":
                result = execute_paper_reproduction(file_bytes, file_name)
            
            if result:
                st.session_state[res_key] = result
                st.session_state[name_key] = file_name
                save_result(cache_key, mode, "", result)
    
    current_result = st.session_state.get(res_key, "")
    if current_result:
        st.markdown(clean_markdown_text(current_result))


def main():
    init_session()
    render_sidebar()
    url, mode, question, btn, learning_mode, paper_file = render_ui()
    
    if learning_mode == "技术文档学习":
        handle_document_analysis(url, mode, question, btn)
    else:
        handle_paper_analysis(paper_file, mode, btn)


if __name__ == "__main__":
    main()