import streamlit as st
from docstudy.parsers.pdf_parser import extract_text_from_pdf
from docstudy.agents.agent import call_llm
from docstudy.prompts.paper_prompt import (
    build_paper_summary_prompt,
    build_paper_innovation_prompt,
    build_paper_tech_route_prompt,
    build_paper_reproduction_prompt
)


def check_stop():
    if st.session_state.stop_analysis:
        print("[APP] Analysis stopped by user")
        st.session_state.stop_analysis = False
        return True
    return False


def execute_paper_summary(file_bytes, file_name):
    print("[APP] Starting paper summary analysis")
    
    if check_stop():
        return ""
    
    with st.spinner("正在解析PDF文件..."):
        if check_stop():
            return ""
        print("[APP] Extracting text from PDF...")
        text, extract_error = extract_text_from_pdf(file_bytes, file_name)
        
        if extract_error:
            print("[APP] PDF extraction failed:", extract_error)
            st.error(f"❌ PDF解析失败：{extract_error}")
            return ""
        
        print("[APP] PDF content extracted, length:", len(text), "characters")
    
    with st.spinner("正在构建Prompt..."):
        if check_stop():
            return ""
        print("[APP] Building paper summary prompt...")
        prompt = build_paper_summary_prompt(text)
        print("[APP] Prompt built, length:", len(prompt), "characters")
    
    with st.spinner("正在调用DeepSeek大模型..."):
        if check_stop():
            return ""
        print("[APP] Calling DeepSeek LLM...")
        result = call_llm(prompt)
        print("[APP] LLM response received, length:", len(result), "characters")
    
    print("[APP] Paper summary analysis completed successfully!\n")
    return result


def execute_paper_innovation(file_bytes, file_name):
    print("[APP] Starting paper innovation analysis")
    
    if check_stop():
        return ""
    
    with st.spinner("正在解析PDF文件..."):
        if check_stop():
            return ""
        print("[APP] Extracting text from PDF...")
        text, extract_error = extract_text_from_pdf(file_bytes, file_name)
        
        if extract_error:
            print("[APP] PDF extraction failed:", extract_error)
            st.error(f"❌ PDF解析失败：{extract_error}")
            return ""
        
        print("[APP] PDF content extracted, length:", len(text), "characters")
    
    with st.spinner("正在构建Prompt..."):
        if check_stop():
            return ""
        print("[APP] Building paper innovation prompt...")
        prompt = build_paper_innovation_prompt(text)
        print("[APP] Prompt built, length:", len(prompt), "characters")
    
    with st.spinner("正在调用DeepSeek大模型..."):
        if check_stop():
            return ""
        print("[APP] Calling DeepSeek LLM...")
        result = call_llm(prompt)
        print("[APP] LLM response received, length:", len(result), "characters")
    
    print("[APP] Paper innovation analysis completed successfully!\n")
    return result


def execute_paper_tech_route(file_bytes, file_name):
    print("[APP] Starting paper tech route analysis")
    
    if check_stop():
        return ""
    
    with st.spinner("正在解析PDF文件..."):
        if check_stop():
            return ""
        print("[APP] Extracting text from PDF...")
        text, extract_error = extract_text_from_pdf(file_bytes, file_name)
        
        if extract_error:
            print("[APP] PDF extraction failed:", extract_error)
            st.error(f"❌ PDF解析失败：{extract_error}")
            return ""
        
        print("[APP] PDF content extracted, length:", len(text), "characters")
    
    with st.spinner("正在构建Prompt..."):
        if check_stop():
            return ""
        print("[APP] Building tech route prompt...")
        prompt = build_paper_tech_route_prompt(text)
        print("[APP] Prompt built, length:", len(prompt), "characters")
    
    with st.spinner("正在调用DeepSeek大模型..."):
        if check_stop():
            return ""
        print("[APP] Calling DeepSeek LLM...")
        result = call_llm(prompt)
        print("[APP] LLM response received, length:", len(result), "characters")
    
    print("[APP] Paper tech route analysis completed successfully!\n")
    return result


def execute_paper_reproduction(file_bytes, file_name):
    print("[APP] Starting paper reproduction guide")
    
    if check_stop():
        return ""
    
    with st.spinner("正在解析PDF文件..."):
        if check_stop():
            return ""
        print("[APP] Extracting text from PDF...")
        text, extract_error = extract_text_from_pdf(file_bytes, file_name)
        
        if extract_error:
            print("[APP] PDF extraction failed:", extract_error)
            st.error(f"❌ PDF解析失败：{extract_error}")
            return ""
        
        print("[APP] PDF content extracted, length:", len(text), "characters")
    
    with st.spinner("正在构建Prompt..."):
        if check_stop():
            return ""
        print("[APP] Building reproduction prompt...")
        prompt = build_paper_reproduction_prompt(text)
        print("[APP] Prompt built, length:", len(prompt), "characters")
    
    with st.spinner("正在调用DeepSeek大模型..."):
        if check_stop():
            return ""
        print("[APP] Calling DeepSeek LLM...")
        result = call_llm(prompt)
        print("[APP] LLM response received, length:", len(result), "characters")
    
    print("[APP] Paper reproduction guide completed successfully!\n")
    return result