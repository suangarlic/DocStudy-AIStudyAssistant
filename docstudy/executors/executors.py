import streamlit as st
from docstudy.parsers.parser import fetch_text, validate_url, is_likely_document
from docstudy.agents.agent import call_llm
from docstudy.prompts.prompt import build_learning_prompt, build_teaching_prompt, build_project_prompt, split_text, build_rag_prompt
from docstudy.utils.rag_utils import keyword_match_context
from docstudy.lesson_builder import build_lesson_video, parse_lesson_script


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
    print("\n[APP] Starting teaching video generation for:", url)
    
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
        
        with st.spinner("正在构建教学脚本Prompt..."):
            if check_stop():
                return ""
            print("[APP] Building teaching prompt...")
            prompt = build_teaching_prompt(text)
            print("[APP] Prompt built, length:", len(prompt), "characters")
        
        with st.spinner("正在调用DeepSeek生成教学脚本..."):
            if check_stop():
                return ""
            print("[APP] Calling DeepSeek LLM...")
            result = call_llm(prompt)
            print("[APP] LLM response received, length:", len(result), "characters")
        
        lines = result.strip().split('\n')
        title = lines[0].strip() if lines else "技术教学"
        script = '\n'.join(lines[1:]).strip() if len(lines) > 1 else result
        
        chapters = parse_lesson_script(result)
        
        if not chapters:
            print("[APP] Failed to parse lesson script, falling back to old format")
            title = "技术教学"
            chapters = [{"title": "课程介绍", "content": result}]
        
        lesson_title = chapters[0].get("title", "技术教学") if chapters else "技术教学"
        
        print(f"[APP] Lesson title: {lesson_title}")
        print(f"[APP] Number of chapters: {len(chapters)}")
        
        DEBUG_MODE = False
        
        if DEBUG_MODE:
            print("[APP] DEBUG MODE: Skipping video generation")
            st.info("📝 调试模式：跳过视频生成，仅显示教学脚本")
            st.subheader("📝 课程标题")
            st.write(lesson_title)
            st.subheader("📝 章节内容")
            for i, chapter in enumerate(chapters):
                st.write(f"**章节 {i+1}: {chapter.get('title', '')}**")
                st.write(chapter.get('content', ''))
            print("[APP] Teaching script generation completed successfully!\n")
            return f"**课程标题：** {lesson_title}\n\n**章节数：** {len(chapters)}"
        
        with st.spinner("正在生成教学视频..."):
            if check_stop():
                return ""
            try:
                video_path = build_lesson_video(lesson_title, chapters)
                print(f"[APP] Video generated: {video_path}")
            except Exception as e:
                print(f"[APP] Video generation failed: {str(e)}")
                st.error(f"❌ 视频生成失败：{str(e)}")
                st.warning("⚠️ 请稍后重试，可能是网络连接问题")
                return ""
        
        print("[APP] Teaching video generation completed successfully!\n")
        return video_path


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