import streamlit as st
from app import rag_pipeline
from memory import record_feedback, get_feedback_summary

st.set_page_config(
    page_title="Crawl4AI Assistant",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'Geist', -apple-system, sans-serif;
    background: #09090b;
    color: #e4e4e7;
    font-size: 14px;
}
.stApp { background: #09090b; }
.main .block-container { max-width: 860px; padding: 0 24px 120px 24px; margin: 0 auto; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 99px; }

/* TOPBAR */
.topbar {
    position: sticky; top: 0; z-index: 100;
    background: rgba(9,9,11,0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid #27272a;
    padding: 0 32px; height: 52px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 32px;
}
.topbar-left { display: flex; align-items: center; gap: 10px; }
.topbar-logo {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    border-radius: 7px; display: flex; align-items: center;
    justify-content: center; font-size: 14px;
    box-shadow: 0 0 0 1px rgba(124,58,237,0.3), 0 4px 12px rgba(124,58,237,0.25);
}
.topbar-name { font-size: 15px; font-weight: 600; color: #fafafa; letter-spacing: -0.02em; }
.topbar-badge {
    font-size: 10px; font-weight: 500; color: #a1a1aa;
    background: #18181b; border: 1px solid #27272a;
    border-radius: 99px; padding: 2px 8px; letter-spacing: 0.03em;
}
.topbar-right { display: flex; align-items: center; gap: 6px; }
.status-dot {
    width: 6px; height: 6px; background: #22c55e;
    border-radius: 50%; box-shadow: 0 0 6px rgba(34,197,94,0.6);
    animation: pulse-dot 2.5s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%,100% { box-shadow: 0 0 6px rgba(34,197,94,0.6); }
    50% { box-shadow: 0 0 12px rgba(34,197,94,0.9); }
}
.status-text { font-size: 11px; color: #71717a; }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #09090b !important;
    border-right: 1px solid #18181b !important;
}
[data-testid="stSidebar"] > div { padding: 20px 16px !important; }
.sidebar-section-title {
    font-size: 10px; font-weight: 600; color: #52525b;
    letter-spacing: 0.08em; text-transform: uppercase;
    padding: 16px 4px 8px;
}
.pipeline-item {
    display: flex; align-items: center; gap: 8px;
    padding: 7px 8px; border-radius: 6px;
    font-size: 12px; color: #a1a1aa;
    transition: background 0.12s;
}
.pipeline-item:hover { background: #18181b; color: #e4e4e7; }
.pipeline-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: #22c55e; flex-shrink: 0;
    box-shadow: 0 0 4px rgba(34,197,94,0.5);
}
.sidebar-stats {
    background: #18181b; border: 1px solid #27272a;
    border-radius: 8px; padding: 12px; margin-top: 4px;
}
.stats-row {
    display: flex; justify-content: space-between;
    align-items: center; padding: 4px 0;
    font-size: 12px; border-bottom: 1px solid #27272a;
}
.stats-row:last-child { border-bottom: none; }
.stats-label { color: #71717a; }
.stats-value { color: #a1a1aa; font-family: 'Geist Mono', monospace; font-size: 11px; }

[data-testid="stSidebar"] [data-testid="stButton"] button {
    width: 100% !important; background: transparent !important;
    border: 1px solid #27272a !important; color: #71717a !important;
    border-radius: 6px !important; font-family: 'Geist', sans-serif !important;
    font-size: 12px !important; font-weight: 400 !important;
    padding: 6px 12px !important; transition: all 0.12s !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: #18181b !important; border-color: #3f3f46 !important; color: #e4e4e7 !important;
}
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: #18181b !important; border: 1px solid #27272a !important;
    border-radius: 8px !important; font-family: 'Geist Mono', monospace !important;
    font-size: 11px !important; color: #71717a !important; padding: 10px !important;
}
[data-testid="stSidebar"] hr { border-color: #18181b !important; margin: 8px 0 !important; }

/* EMPTY STATE */
.empty-state {
    display: flex; flex-direction: column;
    align-items: center; padding: 80px 24px 48px; text-align: center;
}
.empty-icon {
    width: 52px; height: 52px; background: #18181b;
    border: 1px solid #27272a; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; margin-bottom: 20px;
    box-shadow: 0 0 0 1px #27272a, 0 8px 24px rgba(0,0,0,0.4);
}
.empty-title { font-size: 22px; font-weight: 600; color: #fafafa; letter-spacing: -0.03em; margin-bottom: 8px; }
.empty-sub { font-size: 13px; color: #71717a; line-height: 1.6; max-width: 400px; margin-bottom: 32px; }
.suggestions { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; max-width: 600px; }
.suggestion-chip {
    background: #18181b; border: 1px solid #27272a; border-radius: 8px;
    padding: 8px 14px; font-size: 12px; color: #a1a1aa;
    font-family: 'Geist', sans-serif;
}

/* CHAT MESSAGES */
[data-testid="stChatMessage"] {
    background: transparent !important; border: none !important;
    border-radius: 0 !important; padding: 24px 0 !important;
    border-bottom: 1px solid #18181b !important; margin-bottom: 0 !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: #27272a !important; color: #a1a1aa !important;
    border-radius: 7px !important; border: 1px solid #3f3f46 !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #fff !important; border-radius: 7px !important;
    box-shadow: 0 0 0 1px rgba(124,58,237,0.3) !important;
}
[data-testid="stChatMessage"] p {
    font-family: 'Geist', sans-serif !important; font-size: 14px !important;
    line-height: 1.75 !important; color: #d4d4d8 !important;
}
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    font-family: 'Geist', sans-serif !important; font-weight: 600 !important;
    color: #fafafa !important; letter-spacing: -0.02em !important; margin: 20px 0 8px !important;
}
[data-testid="stChatMessage"] h1 { font-size: 18px !important; }
[data-testid="stChatMessage"] h2 { font-size: 15px !important; }
[data-testid="stChatMessage"] h3 { font-size: 14px !important; }
[data-testid="stChatMessage"] code {
    font-family: 'Geist Mono', monospace !important;
    background: #18181b !important; color: #a78bfa !important;
    border: 1px solid #27272a !important; border-radius: 4px !important;
    padding: 1px 5px !important; font-size: 12px !important;
}
[data-testid="stChatMessage"] pre {
    background: #18181b !important; border: 1px solid #27272a !important;
    border-radius: 8px !important; padding: 16px !important; margin: 12px 0 !important;
}
[data-testid="stChatMessage"] pre code {
    background: transparent !important; border: none !important;
    color: #d4d4d8 !important; font-size: 12px !important; padding: 0 !important;
}
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol {
    padding-left: 18px !important; color: #d4d4d8 !important;
    font-size: 14px !important; line-height: 1.8 !important;
}
[data-testid="stChatMessage"] strong { color: #fafafa !important; font-weight: 500 !important; }
[data-testid="stChatMessage"] blockquote {
    border-left: 2px solid #3f3f46 !important;
    padding-left: 14px !important; color: #71717a !important; margin: 8px 0 !important;
}

/* FEEDBACK BUTTONS */
[data-testid="stButton"] button {
    font-family: 'Geist', sans-serif !important; font-size: 12px !important;
    font-weight: 400 !important; background: transparent !important;
    border: 1px solid #27272a !important; color: #52525b !important;
    border-radius: 6px !important; padding: 3px 10px !important; transition: all 0.12s !important;
}
[data-testid="stButton"] button:hover {
    background: #18181b !important; border-color: #3f3f46 !important; color: #a1a1aa !important;
}
.stCaption p, .stCaption small {
    font-family: 'Geist', sans-serif !important; font-size: 11px !important; color: #52525b !important;
}

/* CHAT INPUT */
[data-testid="stChatInput"] {
    background: #18181b !important; border: 1px solid #27272a !important;
    border-radius: 10px !important;
    box-shadow: 0 0 0 1px #27272a, 0 4px 20px rgba(0,0,0,0.4) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 1px #7c3aed, 0 4px 24px rgba(124,58,237,0.15) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Geist', sans-serif !important; font-size: 14px !important;
    color: #e4e4e7 !important; background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #3f3f46 !important; font-size: 13px !important; }

hr { border-color: #18181b !important; }
em { color: #71717a !important; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# Topbar
st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div class="topbar-logo">🕸️</div>
        <span class="topbar-name">Crawl4AI</span>
        <span class="topbar-badge">DOCS</span>
    </div>
    <div class="topbar-right">
        <div class="status-dot"></div>
        <span class="status-text">All systems operational</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-section-title">Retrieval Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
    <div>
        <div class="pipeline-item"><span class="pipeline-dot"></span>Semantic search · Pinecone</div>
        <div class="pipeline-item"><span class="pipeline-dot"></span>BM25 keyword search</div>
        <div class="pipeline-item"><span class="pipeline-dot"></span>Reciprocal Rank Fusion</div>
        <div class="pipeline-item"><span class="pipeline-dot"></span>Cross-encoder reranking</div>
        <div class="pipeline-item"><span class="pipeline-dot"></span>Short + long-term memory</div>
        <div class="pipeline-item"><span class="pipeline-dot"></span>Query rewriting · LLM</div>
        <div class="pipeline-item"><span class="pipeline-dot"></span>Hallucination guard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Model Info</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-stats">
        <div class="stats-row"><span class="stats-label">LLM</span><span class="stats-value">llama-3.1-8b</span></div>
        <div class="stats-row"><span class="stats-label">Embeddings</span><span class="stats-value">MiniLM-L6-v2</span></div>
        <div class="stats-row"><span class="stats-label">Reranker</span><span class="stats-value">ms-marco</span></div>
        <div class="stats-row"><span class="stats-label">Provider</span><span class="stats-value">Groq · Pinecone</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Session</div>', unsafe_allow_html=True)
    if st.button("↺  New conversation"):
        st.session_state.messages = []
        st.session_state.feedback = {}
        st.rerun()

    st.markdown('<div class="sidebar-section-title">Feedback</div>', unsafe_allow_html=True)
    st.info(get_feedback_summary())

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🕸️</div>
        <div class="empty-title">Crawl4AI Documentation</div>
        <div class="empty-sub">
            Ask anything about the Crawl4AI library — installation, async crawling,
            structured extraction, hooks, or the full API reference.
        </div>
        <div class="suggestions">
            <div class="suggestion-chip">How do I install Crawl4AI?</div>
            <div class="suggestion-chip">Explain AsyncWebCrawler</div>
            <div class="suggestion-chip">How to extract structured data?</div>
            <div class="suggestion-chip">CSS selectors in extraction</div>
            <div class="suggestion-chip">What is CrawlResult?</div>
            <div class="suggestion-chip">How to handle JavaScript pages?</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            feedback_key = f"feedback_{i}"
            if feedback_key not in st.session_state.feedback:
                col1, col2, _ = st.columns([1, 1, 10])
                with col1:
                    if st.button("👍", key=f"up_{i}"):
                        st.session_state.feedback[feedback_key] = True
                        user_query = ""
                        if i > 0 and st.session_state.messages[i-1]["role"] == "user":
                            user_query = st.session_state.messages[i-1]["content"]
                        record_feedback(user_query, msg["content"], was_helpful=True)
                        st.rerun()
                with col2:
                    if st.button("👎", key=f"down_{i}"):
                        st.session_state.feedback[feedback_key] = False
                        user_query = ""
                        if i > 0 and st.session_state.messages[i-1]["role"] == "user":
                            user_query = st.session_state.messages[i-1]["content"]
                        record_feedback(user_query, msg["content"], was_helpful=False)
                        st.rerun()
            else:
                val = st.session_state.feedback[feedback_key]
                st.caption("✅ Helpful" if val else "❌ Not helpful")

# Input
user_input = st.chat_input("Message Crawl4AI assistant...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""
        placeholder.markdown("_Retrieving documentation..._")
        for token in rag_pipeline(user_input):
            response += token
            placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
