import os
import json
import streamlit as st


RESULT_CACHE_DIR = "result_cache"


DOCUMENT_MODES = ["学习路线分析", "入门讲解", "实践项目练手", "开发者问答"]
PAPER_MODES = ["论文速读", "创新点分析", "技术路线拆解", "复现指南"]


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


def get_all_records():
    records = []
    if not os.path.exists(RESULT_CACHE_DIR):
        return records
    
    for filename in os.listdir(RESULT_CACHE_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(RESULT_CACHE_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                record = {
                    "url": data.get("url", ""),
                    "mode": data.get("mode", ""),
                    "question": data.get("question", ""),
                    "result": data.get("result", ""),
                    "timestamp": os.path.getmtime(filepath),
                    "filename": filename
                }
                records.append(record)
            except Exception:
                continue
    
    records.sort(key=lambda x: x["timestamp"], reverse=True)
    return records


def get_document_history():
    records = get_all_records()
    return [r for r in records if r["mode"] in DOCUMENT_MODES]


def get_paper_history():
    records = get_all_records()
    return [r for r in records if r["mode"] in PAPER_MODES]


def get_statistics(records):
    document_count = 0
    paper_count = 0
    
    for record in records:
        mode = record["mode"]
        if mode in DOCUMENT_MODES:
            document_count += 1
        elif mode in PAPER_MODES:
            paper_count += 1
    
    return {
        "document_count": document_count,
        "paper_count": paper_count,
        "total_count": len(records)
    }


def get_learning_level(total_count):
    if total_count < 5:
        return {"level": "Lv1", "title": "新手", "emoji": "🌱", "color": "#9E9E9E"}
    elif total_count < 15:
        return {"level": "Lv2", "title": "学习者", "emoji": "📚", "color": "#4CAF50"}
    elif total_count < 30:
        return {"level": "Lv3", "title": "技术探索者", "emoji": "🔍", "color": "#2196F3"}
    else:
        return {"level": "Lv4", "title": "技术专家", "emoji": "🏆", "color": "#FF9800"}


def restore_history(record):
    mode = record["mode"]
    url = record["url"]
    result = record["result"]
    question = record["question"]
    
    if mode not in SESSION_KEYS:
        return
    
    res_key, url_key = SESSION_KEYS[mode]
    
    st.session_state[res_key] = result
    st.session_state[url_key] = url
    
    if mode == "开发者问答":
        st.session_state.last_question = question
    
    if mode in DOCUMENT_MODES:
        st.session_state["selected_mode"] = mode
        st.session_state["selected_learning_mode"] = "技术文档学习"
        if url:
            st.session_state["selected_url"] = url
    else:
        st.session_state["selected_mode"] = mode
        st.session_state["selected_learning_mode"] = "论文学习"
        if url.startswith("paper_"):
            st.session_state["selected_paper_name"] = url.replace("paper_", "").split("_")[0]
            st.session_state[url_key] = url.replace("paper_", "").split("_")[0]


def delete_history(record):
    filename = record["filename"]
    filepath = os.path.join(RESULT_CACHE_DIR, filename)
    
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"[APP] Deleted history record: {filename}")
            
            mode = record["mode"]
            if mode in SESSION_KEYS:
                res_key, url_key = SESSION_KEYS[mode]
                if st.session_state.get(res_key) == record.get("result"):
                    st.session_state[res_key] = ""
                    st.session_state[url_key] = ""
            
            return True
    except Exception as e:
        print(f"[APP] Error deleting history record: {e}")
    
    return False


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 16px; margin-bottom: 20px;">
            <h3 style="color: white; margin: 0;">📚 我的学习中心</h3>
        </div>
        """, unsafe_allow_html=True)
        
        records = get_all_records()
        stats = get_statistics(records)
        level = get_learning_level(stats["total_count"])
        
        st.markdown("""
        <div style="border-left: 4px solid #FF9800; padding: 8px 12px; margin-bottom: 16px;">
            <h4 style="margin: 0;">📖 分类历史</h4>
        </div>
        """, unsafe_allow_html=True)
        
        doc_history = get_document_history()
        paper_history = get_paper_history()
        
        with st.expander(f"📖 文档学习历史 ({len(doc_history)})", expanded=False):
            if doc_history:
                for record in doc_history:
                    mode = record["mode"]
                    url = record["url"]
                    timestamp = record["timestamp"]
                    display_text = url[:40] + "..." if len(url) > 40 else url
                    
                    import datetime
                    time_str = datetime.datetime.fromtimestamp(timestamp).strftime("%m-%d %H:%M")
                    
                    st.markdown(f"""
                    <div style="padding: 8px; background: #f5f5f5; border-radius: 8px; margin-bottom: 8px;">
                        <div style="font-size: 12px; color: #999; margin-bottom: 4px;">{time_str}</div>
                        <div style="font-size: 13px; color: #666; margin-bottom: 4px;">{mode}</div>
                        <div style="font-size: 14px; color: #333; font-weight: 500; word-break: break-all;">{display_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        if st.button("🔄 恢复", key=f"doc_{record['filename']}_restore", 
                                   use_container_width=True, help="恢复此记录"):
                            restore_history(record)
                            st.success(f"已恢复：{mode}")
                    with col2:
                        if st.button("🗑️", key=f"doc_{record['filename']}_delete", 
                                   use_container_width=True, help="删除此记录"):
                            if delete_history(record):
                                st.success("已删除")
            else:
                st.markdown("""
                <div style="text-align: center; padding: 16px; color: #999; font-size: 13px;">
                    <div style="font-size: 24px; margin-bottom: 8px;">📄</div>
                    暂无文档学习记录
                    <div style="font-size: 11px; margin-top: 4px;">开始分析技术文档吧！</div>
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander(f"📄 论文学习历史 ({len(paper_history)})", expanded=False):
            if paper_history:
                for record in paper_history:
                    mode = record["mode"]
                    url = record["url"]
                    timestamp = record["timestamp"]
                    
                    if url.startswith("paper_"):
                        display_text = url.replace("paper_", "").split("_")[0]
                    else:
                        display_text = url[:40] + "..." if len(url) > 40 else url
                    
                    import datetime
                    time_str = datetime.datetime.fromtimestamp(timestamp).strftime("%m-%d %H:%M")
                    
                    st.markdown(f"""
                    <div style="padding: 8px; background: #f5f5f5; border-radius: 8px; margin-bottom: 8px;">
                        <div style="font-size: 12px; color: #999; margin-bottom: 4px;">{time_str}</div>
                        <div style="font-size: 13px; color: #666; margin-bottom: 4px;">{mode}</div>
                        <div style="font-size: 14px; color: #333; font-weight: 500; word-break: break-all;">{display_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        if st.button("🔄 恢复", key=f"paper_{record['filename']}_restore",
                                   use_container_width=True, help="恢复此记录"):
                            restore_history(record)
                            st.success(f"已恢复：{mode}")
                    with col2:
                        if st.button("🗑️", key=f"paper_{record['filename']}_delete",
                                   use_container_width=True, help="删除此记录"):
                            if delete_history(record):
                                st.success("已删除")
            else:
                st.markdown("""
                <div style="text-align: center; padding: 16px; color: #999; font-size: 13px;">
                    <div style="font-size: 24px; margin-bottom: 8px;">📝</div>
                    暂无论文学习记录
                    <div style="font-size: 11px; margin-top: 4px;">上传论文PDF开始学习吧！</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="border-left: 4px solid #2196F3; padding: 8px 12px; margin-bottom: 16px;">
            <h4 style="margin: 0;">📊 学习统计</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 12px; background: #e3f2fd; border-radius: 8px;">
                <div style="font-size: 24px; font-weight: bold; color: #1976D2;">📄</div>
                <div style="font-size: 18px; font-weight: bold; color: #333;">{stats['document_count']}</div>
                <div style="font-size: 11px; color: #666;">技术文档</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 12px; background: #e8f5e9; border-radius: 8px;">
                <div style="font-size: 24px; font-weight: bold; color: #388E3C;">📝</div>
                <div style="font-size: 18px; font-weight: bold; color: #333;">{stats['paper_count']}</div>
                <div style="font-size: 11px; color: #666;">论文</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 12px; background: #fff3e0; border-radius: 8px;">
                <div style="font-size: 24px; font-weight: bold; color: #F57C00;">🔢</div>
                <div style="font-size: 18px; font-weight: bold; color: #333;">{stats['total_count']}</div>
                <div style="font-size: 11px; color: #666;">总次数</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="border-left: 4px solid #FF5722; padding: 8px 12px; margin-bottom: 16px;">
            <h4 style="margin: 0;">🏆 学习等级</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {level['color']}20 0%, {level['color']}40 100%); 
                    border-radius: 16px; border: 2px solid {level['color']};">
            <div style="font-size: 48px;">{level['emoji']}</div>
            <div style="font-size: 24px; font-weight: bold; color: {level['color']}; margin-top: 8px;">{level['level']}</div>
            <div style="font-size: 16px; color: #333; margin-top: 4px;">{level['title']}</div>
            <div style="font-size: 12px; color: #666; margin-top: 8px;">
                已完成 {stats['total_count']} 次分析
            </div>
        </div>
        """, unsafe_allow_html=True)