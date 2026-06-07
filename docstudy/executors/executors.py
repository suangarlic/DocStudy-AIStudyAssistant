import streamlit as st
from docstudy.parsers.parser import fetch_text, validate_url, is_likely_document
from docstudy.agents.agent import call_llm
from docstudy.prompts.prompt import build_learning_prompt, build_teaching_prompt, build_project_prompt, split_text, build_rag_prompt
from docstudy.utils.rag_utils import keyword_match_context


def check_stop():
    if st.session_state.stop_analysis:
        print("[APP] Analysis stopped by user")
        st.session_state.stop_analysis = False
        return True
    return False


def execute_learning(url):
    print("\n[APP] Starting learning route analysis for:", url)
    
    if check_stop():
        return ""
    
    valid, error_msg = validate_url(url)
    if not valid:
        print("[APP] URL validation failed:", error_msg)
        st.error(f"❌ {error_msg}")
        return ""
    
    with st.spinner("正在抓取网页内容..."):
        if check_stop():
            return ""
        print("[APP] Fetching web page content...")
        text, fetch_error = fetch_text(url)
        
        if fetch_error:
            print("[APP] Fetch failed:", fetch_error)
            st.error(f"❌ 抓取网页失败：{fetch_error}")
            return ""
        
        print("[APP] Page content fetched, length:", len(text), "characters")
        
        is_doc, doc_warning = is_likely_document(text)
        if not is_doc:
            print("[APP] Document validation failed:", doc_warning)
            st.warning(f"⚠️ {doc_warning}")
            st.info("💡 请确认您输入的是技术文档链接，例如：\n- https://docs.python.org/\n- https://react.dev/docs\n- https://github.com/xxx/xxx/blob/main/README.md")
        
        with st.spinner("正在构建Prompt..."):
            if check_stop():
                return ""
            print("[APP] Building learning prompt...")
            prompt = build_learning_prompt(text)
            print("[APP] Prompt built, length:", len(prompt), "characters")
        
        with st.spinner("正在调用DeepSeek大模型..."):
            if check_stop():
                return ""
            print("[APP] Calling DeepSeek LLM...")
            result = call_llm(prompt)
            print("[APP] LLM response received, length:", len(result), "characters")
        
        print("[APP] Learning route analysis completed successfully!\n")
        return result


def execute_teaching(url):
    print("\n[APP] Starting teaching explanation for:", url)
    
    if check_stop():
        return ""
    
    valid, error_msg = validate_url(url)
    if not valid:
        print("[APP] URL validation failed:", error_msg)
        st.error(f"❌ {error_msg}")
        return ""
    
    with st.spinner("正在抓取网页内容..."):
        if check_stop():
            return ""
        print("[APP] Fetching web page content...")
        text, fetch_error = fetch_text(url)
        
        if fetch_error:
            print("[APP] Fetch failed:", fetch_error)
            st.error(f"❌ 抓取网页失败：{fetch_error}")
            return ""
        
        print("[APP] Page content fetched, length:", len(text), "characters")
        
        is_doc, doc_warning = is_likely_document(text)
        if not is_doc:
            print("[APP] Document validation failed:", doc_warning)
            st.warning(f"⚠️ {doc_warning}")
        
        with st.spinner("正在构建教学Prompt..."):
            if check_stop():
                return ""
            print("[APP] Building teaching prompt...")
            prompt = build_teaching_prompt(text)
            print("[APP] Prompt built, length:", len(prompt), "characters")
        
        with st.spinner("正在调用DeepSeek大模型..."):
            if check_stop():
                return ""
            print("[APP] Calling DeepSeek LLM...")
            result = call_llm(prompt)
            print("[APP] LLM response received, length:", len(result), "characters")
        
        print("[APP] Teaching explanation completed successfully!\n")
        return result


def execute_project(url):
    print("\n[APP] Starting project generation for:", url)
    
    if check_stop():
        return ""
    
    valid, error_msg = validate_url(url)
    if not valid:
        print("[APP] URL validation failed:", error_msg)
        st.error(f"❌ {error_msg}")
        return ""
    
    with st.spinner("正在抓取网页内容..."):
        if check_stop():
            return ""
        print("[APP] Fetching web page content...")
        text, fetch_error = fetch_text(url)
        
        if fetch_error:
            print("[APP] Fetch failed:", fetch_error)
            st.error(f"❌ 抓取网页失败：{fetch_error}")
            return ""
        
        print("[APP] Page content fetched, length:", len(text), "characters")
        
        is_doc, doc_warning = is_likely_document(text)
        if not is_doc:
            print("[APP] Document validation failed:", doc_warning)
            st.warning(f"⚠️ {doc_warning}")
        
        with st.spinner("正在构建项目Prompt..."):
            if check_stop():
                return ""
            print("[APP] Building project prompt...")
            prompt = build_project_prompt(text)
            print("[APP] Prompt built, length:", len(prompt), "characters")
        
        with st.spinner("正在调用DeepSeek大模型..."):
            if check_stop():
                return ""
            print("[APP] Calling DeepSeek LLM...")
            result = call_llm(prompt)
            print("[APP] LLM response received, length:", len(result), "characters")
        
        print("[APP] Project generation completed successfully!\n")
        return result


def execute_qa(url, question):
    print("\n[APP] Starting developer Q&A for:", url)
    
    if check_stop():
        return ""
    
    if not question:
        print("[APP] Question input is empty")
        st.error("❌ 请输入您的问题")
        return ""
    
    st.session_state.last_question = question
    
    valid, error_msg = validate_url(url)
    if not valid:
        print("[APP] URL validation failed:", error_msg)
        st.error(f"❌ {error_msg}")
        return ""
    
    with st.spinner("正在抓取网页内容..."):
        if check_stop():
            return ""
        print("[APP] Fetching web page content...")
        text, fetch_error = fetch_text(url)
        
        if fetch_error:
            print("[APP] Fetch failed:", fetch_error)
            st.error(f"❌ 抓取网页失败：{fetch_error}")
            return ""
        
        print("[APP] Page content fetched, length:", len(text), "characters")
        
        with st.spinner("正在切分文档..."):
            if check_stop():
                return ""
            print("[APP] Splitting text into chunks...")
            chunks = split_text(text)
            print("[APP] Generated", len(chunks), "chunks")
            context = keyword_match_context(chunks, question)
            print("[APP] Context length:", len(context), "characters")
        
        with st.spinner("正在构建RAG Prompt..."):
            if check_stop():
                return ""
            print("[APP] Building RAG prompt...")
            prompt = build_rag_prompt(context, question)
            print("[APP] Prompt built, length:", len(prompt), "characters")
        
        with st.spinner("正在调用DeepSeek大模型..."):
            if check_stop():
                return ""
            print("[APP] Calling DeepSeek LLM...")
            result = call_llm(prompt)
            print("[APP] LLM response received, length:", len(result), "characters")
        
        print("[APP] Developer Q&A completed successfully!\n")
        return result