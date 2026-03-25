import streamlit as st
from app import rag_pipeline
from memory import record_feedback, get_feedback_summary

st.set_page_config(
    page_title="WebCrawl AI — Docs Assistant",
    page_icon="🔎",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Space Mono', monospace;
    background-color: #0a0a0f;
    color: #c8c8d4;
}

.stApp {
    background: #0a0a0f;
}

/* ── Animated grain overlay ── */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.6;
}

/* ── Title ── */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
    letter-spacing: -0.03em !important;
    color: #f0f0ff !important;
    padding-bottom: 0 !important;
}

/* ── Caption ── */
.stApp .stCaption p {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #4a9eff;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-left: 2px solid #4a9eff;
    padding-left: 8px;
    margin-top: -4px;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #111118 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
    margin-bottom: 8px !important;
    position: relative;
}

/* User message accent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 3px solid #4a9eff !important;
    background: #0d0d1a !important;
}

/* Assistant message accent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left: 3px solid #00ffaa !important;
    background: #0a0f0d !important;
}

/* ── Avatar icons ── */
[data-testid="chatAvatarIcon-user"] {
    background: #1a1a3e !important;
    color: #4a9eff !important;
}

[data-testid="chatAvatarIcon-assistant"] {
    background: #0a1f16 !important;
    color: #00ffaa !important;
}

/* ── Message text ── */
[data-testid="stChatMessage"] p {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.75 !important;
    color: #c8c8d4 !important;
}

/* Code blocks inside chat */
[data-testid="stChatMessage"] code {
    background: #1a1a2e !important;
    color: #00ffaa !important;
    border-radius: 3px !important;
    padding: 1px 5px !important;
    font-size: 0.78rem !important;
}

[data-testid="stChatMessage"] pre {
    background: #0d0d1a !important;
    border: 1px solid #1e1e3e !important;
    border-radius: 4px !important;
    padding: 12px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #111118 !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 4px !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #4a9eff !important;
    box-shadow: 0 0 0 2px rgba(74, 158, 255, 0.15) !important;
}

[data-testid="stChatInput"] textarea {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    color: #e0e0f0 !important;
    background: transparent !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #3a3a5a !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #080810 !important;
    border-right: 1px solid #1e1e2e !important;
}

[data-testid="stSidebar"] h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #4a9eff !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #7a7a9a !important;
    line-height: 1.8 !important;
}

[data-testid="stSidebar"] strong {
    color: #c8c8d4 !important;
}

/* Sidebar info box */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: #0d0d1a !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
}

/* ── Buttons (feedback) ── */
[data-testid="stButton"] button {
    background: #111118 !important;
    border: 1px solid #2a2a3e !important;
    color: #7a7a9a !important;
    border-radius: 3px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    padding: 2px 10px !important;
    transition: all 0.15s ease !important;
}

[data-testid="stButton"] button:hover {
    border-color: #4a9eff !important;
    color: #4a9eff !important;
    background: #0d1020 !important;
}

/* Clear chat button special */
[data-testid="stSidebar"] [data-testid="stButton"] button {
    width: 100% !important;
    border-color: #3a1a1a !important;
    color: #aa4444 !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    border-color: #ff4444 !important;
    color: #ff4444 !important;
    background: #1a0a0a !important;
}

/* ── Caption (feedback labels) ── */
.stCaption small, .stCaption p {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
}

/* ── Divider ── */
hr {
    border-color: #1e1e2e !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a4e; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #4a9eff; }

/* ── Blinking cursor on title ── */
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 0.2rem; padding-top: 0.5rem;">
    <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a3a5a; letter-spacing:0.15em; margin-bottom:6px;">
        ▸ SYSTEM ONLINE · CRAWL4AI DOCS v2.0
    </div>
    <h1 style="font-family:'Syne',sans-serif; font-weight:800; font-size:1.8rem; color:#f0f0ff; margin:0; letter-spacing:-0.03em;">
        WebCrawl<span style="color:#4a9eff;">_</span>AI
        <span style="font-size:1rem; color:#00ffaa; font-family:'Space Mono',monospace; font-weight:400;">docs</span>
    </h1>
</div>
""", unsafe_allow_html=True)

st.caption("HYBRID SEARCH · CROSS-ENCODER RERANKING · SELF-IMPROVING RAG")

st.markdown("<div style='height:1px; background:linear-gradient(90deg,#4a9eff22,#00ffaa22,transparent); margin-bottom:1rem;'></div>", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.6rem; color:#3a3a5a; letter-spacing:0.15em; padding: 8px 0 4px;">
        ◈ PIPELINE STATUS
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.7rem; line-height:2; color:#5a5a7a; padding: 4px 0;">
        <span style="color:#00ffaa;">✓</span> Semantic · Pinecone<br>
        <span style="color:#00ffaa;">✓</span> Keyword · BM25<br>
        <span style="color:#00ffaa;">✓</span> Rank Fusion · RRF<br>
        <span style="color:#00ffaa;">✓</span> Reranker · Cross-Encoder<br>
        <span style="color:#00ffaa;">✓</span> Memory · Short + Long<br>
        <span style="color:#00ffaa;">✓</span> Query Rewriter<br>
        <span style="color:#00ffaa;">✓</span> Hallucination Guard<br>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("⌫  Clear session"):
        st.session_state.messages = []
        st.session_state.feedback = {}
        st.rerun()

    st.divider()

    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.6rem; color:#3a3a5a; letter-spacing:0.15em; padding-bottom:4px;">
        ◈ FEEDBACK LOG
    </div>
    """, unsafe_allow_html=True)
    st.info(get_feedback_summary())

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
user_input = st.chat_input("› query docs: installation, crawling, API, extraction ...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""

        placeholder.markdown("_`scanning vector index...`_")

        for token in rag_pipeline(user_input):
            response += token
            placeholder.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()
