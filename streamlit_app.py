import streamlit as st
from app import rag_pipeline
from memory import record_feedback, get_feedback_summary

st.set_page_config(
    page_title="Crawl4AI Assistant",
    page_icon="🕸️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f9f7f4;
    color: #1a1a1a;
}

.stApp {
    background-color: #f9f7f4;
}

.main .block-container {
    max-width: 720px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

/* ── Title ── */
h1 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.4rem !important;
    color: #1a1a1a !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0 !important;
}

.stApp .stCaption p {
    font-size: 0.75rem !important;
    color: #999 !important;
    margin-top: 2px !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 20px 0 !important;
    border-bottom: 1px solid #f0ede8 !important;
    margin-bottom: 0 !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p {
    font-weight: 500 !important;
    color: #1a1a1a !important;
}

/* ── Avatars ── */
[data-testid="chatAvatarIcon-user"] {
    background: #e8632a !important;
    color: #fff !important;
    border-radius: 6px !important;
}

[data-testid="chatAvatarIcon-assistant"] {
    background: #1a1a1a !important;
    color: #fff !important;
    border-radius: 6px !important;
}

/* ── Message text ── */
[data-testid="stChatMessage"] p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.75 !important;
    color: #2a2a2a !important;
}

[data-testid="stChatMessage"] code {
    background: #f0ede8 !important;
    color: #c4370a !important;
    border-radius: 4px !important;
    padding: 1px 6px !important;
    font-size: 0.82rem !important;
    font-family: 'SF Mono', 'Fira Code', monospace !important;
}

[data-testid="stChatMessage"] pre {
    background: #1e1e1e !important;
    border-radius: 10px !important;
    padding: 16px !important;
    border: none !important;
}

[data-testid="stChatMessage"] pre code {
    background: transparent !important;
    color: #e8e8e8 !important;
    font-size: 0.8rem !important;
}

/* ── Chat Input ── */
[data-testid="stChatInput"] {
    background: #fff !important;
    border: 1.5px solid #e8e2d9 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #e8632a !important;
    box-shadow: 0 2px 16px rgba(232, 99, 42, 0.12) !important;
}

[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    color: #1a1a1a !important;
    background: transparent !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #bbb !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #fff !important;
    border-right: 1px solid #f0ede8 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    color: #555 !important;
    line-height: 1.9 !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: #fdf6f2 !important;
    border: 1px solid #f5ddd2 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
}

/* ── Buttons ── */
[data-testid="stButton"] button {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    background: #fff !important;
    border: 1.5px solid #e8e2d9 !important;
    color: #555 !important;
    border-radius: 8px !important;
    transition: all 0.15s !important;
}

[data-testid="stButton"] button:hover {
    border-color: #e8632a !important;
    color: #e8632a !important;
    background: #fdf6f2 !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button {
    width: 100% !important;
}

/* ── Divider ── */
hr {
    border-color: #f0ede8 !important;
    margin: 12px 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #e8e2d9; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #e8632a; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:4px; padding-top:8px;">
    <div style="width:34px; height:34px; background:#1a1a1a; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:17px; flex-shrink:0;">🕸️</div>
    <div>
        <div style="font-family:'Inter',sans-serif; font-weight:600; font-size:1.05rem; color:#1a1a1a; letter-spacing:-0.02em; line-height:1.3;">
            Crawl4AI Docs
        </div>
        <div style="font-family:'Inter',sans-serif; font-size:0.7rem; color:#aaa; line-height:1.3;">
            Documentation assistant
        </div>
    </div>
</div>
<div style="height:1px; background:#f0ede8; margin:12px 0 8px;"></div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 8px;">
        <div style="font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:600; color:#bbb; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:10px;">
            Pipeline
        </div>
        <div style="font-family:'Inter',sans-serif; font-size:0.78rem; line-height:2.1; color:#555;">
            <span style="display:inline-block; width:7px; height:7px; background:#22c55e; border-radius:50%; margin-right:8px;"></span>Semantic search · Pinecone<br>
            <span style="display:inline-block; width:7px; height:7px; background:#22c55e; border-radius:50%; margin-right:8px;"></span>BM25 keyword search<br>
            <span style="display:inline-block; width:7px; height:7px; background:#22c55e; border-radius:50%; margin-right:8px;"></span>Reciprocal Rank Fusion<br>
            <span style="display:inline-block; width:7px; height:7px; background:#22c55e; border-radius:50%; margin-right:8px;"></span>Cross-encoder reranking<br>
            <span style="display:inline-block; width:7px; height:7px; background:#22c55e; border-radius:50%; margin-right:8px;"></span>Short + long-term memory<br>
            <span style="display:inline-block; width:7px; height:7px; background:#22c55e; border-radius:50%; margin-right:8px;"></span>Query rewriting<br>
            <span style="display:inline-block; width:7px; height:7px; background:#22c55e; border-radius:50%; margin-right:8px;"></span>Hallucination guard<br>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.feedback = {}
        st.rerun()

    st.divider()

    st.markdown("""
    <div style="font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:600; color:#bbb; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:6px;">
        Feedback
    </div>
    """, unsafe_allow_html=True)
    st.info(get_feedback_summary())

# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding:52px 0 28px;">
        <div style="font-size:2.4rem; margin-bottom:14px;">🕸️</div>
        <div style="font-family:'Inter',sans-serif; font-size:1.25rem; font-weight:600; color:#1a1a1a; margin-bottom:6px; letter-spacing:-0.02em;">
            How can I help?
        </div>
        <div style="font-family:'Inter',sans-serif; font-size:0.85rem; color:#aaa; max-width:380px; margin:0 auto; line-height:1.6;">
            Ask me anything about Crawl4AI — installation, crawling, extraction, or the API.
        </div>
    </div>
    <div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:36px;">
        <div style="background:#fff; border:1.5px solid #f0ede8; border-radius:10px; padding:9px 15px; font-family:'Inter',sans-serif; font-size:0.78rem; color:#555; cursor:default;">How do I install Crawl4AI?</div>
        <div style="background:#fff; border:1.5px solid #f0ede8; border-radius:10px; padding:9px 15px; font-family:'Inter',sans-serif; font-size:0.78rem; color:#555; cursor:default;">How to extract structured data?</div>
        <div style="background:#fff; border:1.5px solid #f0ede8; border-radius:10px; padding:9px 15px; font-family:'Inter',sans-serif; font-size:0.78rem; color:#555; cursor:default;">What is AsyncWebCrawler?</div>
        <div style="background:#fff; border:1.5px solid #f0ede8; border-radius:10px; padding:9px 15px; font-family:'Inter',sans-serif; font-size:0.78rem; color:#555; cursor:default;">How to use CSS selectors?</div>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            feedback_key = f"feedback_{i}"
            if feedback_key not in st.session_state.feedback:
                col1, col2, _ = st.columns([1, 1, 8])
                with col1:
                    if st.button("👍", key=f"up_{i}"):
                        st.session_state.feedback[feedback_key] = True
                        user_query = ""
                        if i > 0 and st.session_state.messages[i - 1]["role"] == "user":
                            user_query = st.session_state.messages[i - 1]["content"]
                        record_feedback(user_query, msg["content"], was_helpful=True)
                        st.rerun()
                with col2:
                    if st.button("👎", key=f"down_{i}"):
                        st.session_state.feedback[feedback_key] = False
                        user_query = ""
                        if i > 0 and st.session_state.messages[i - 1]["role"] == "user":
                            user_query = st.session_state.messages[i - 1]["content"]
                        record_feedback(user_query, msg["content"], was_helpful=False)
                        st.rerun()
            else:
                val = st.session_state.feedback[feedback_key]
                st.caption("✅ Helpful" if val else "❌ Not helpful")

# ── Input ─────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask anything about Crawl4AI...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""
        placeholder.markdown("_Searching documentation..._")
        for token in rag_pipeline(user_input):
            response += token
            placeholder.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()
