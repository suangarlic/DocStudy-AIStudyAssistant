import re
import json
import streamlit as st


def extract_learning_route(text):
    pattern = r'```json\s*(\[[\s\S]*?\])\s*```'
    match = re.search(pattern, text)
    
    if match:
        try:
            data = json.loads(match.group(1))
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    
    fallback_pattern = r'\[\s*\{[\s\S]*?\}\s*\]'
    match = re.search(fallback_pattern, text)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    
    return None


def render_learning_route(route_data):
    if not route_data or not isinstance(route_data, list):
        return
    
    stages = []
    for item in route_data:
        stage = {
            "stage": item.get("stage", "未命名阶段"),
            "difficulty": min(max(int(item.get("difficulty", 1)), 1), 5),
            "duration": item.get("duration", "未知")
        }
        stages.append(stage)
    
    for i, stage in enumerate(stages):
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                color: white; font-weight: bold; font-size: 14px;">
                        {i + 1}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 16px; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid #667eea;">
                    <h4 style="margin: 0 0 8px 0; color: #333;">{stage['stage']}</h4>
                    <div style="display: flex; gap: 16px; align-items: center;">
                        <span style="color: #666; font-size: 13px;">
                            <strong style="color: #ff9800;">{'⭐' * stage['difficulty']}{'☆' * (5 - stage['difficulty'])}</strong>
                        </span>
                        <span style="color: #666; font-size: 13px;">
                            ⏱️ {stage['duration']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if i < len(stages) - 1:
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin: -10px 0 20px 0;">
                <svg width="20" height="30" viewBox="0 0 20 30">
                    <path d="M10 0 L10 20 M10 20 L5 15 M10 20 L15 15" 
                          stroke="#ddd" stroke-width="2" fill="none"/>
                    <circle cx="10" cy="25" r="3" fill="#667eea"/>
                </svg>
            </div>
            """, unsafe_allow_html=True)


def clean_markdown_text(text):
    cleaned = re.sub(r'```json\s*[\s\S]*?```\s*', '', text)
    cleaned = re.sub(r'\[\s*\{[\s\S]*?\}\s*\]\s*', '', cleaned)
    return cleaned.strip()


def generate_knowledge_graph(text):
    route_data = extract_learning_route(text)
    if route_data is not None:
        render_learning_route(route_data)
