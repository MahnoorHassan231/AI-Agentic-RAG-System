"""
main.py
-------
Professional UI for AI Agentic RAG System.
Features: Bottom chat input, chat bubbles, agent badges, stats sidebar.
"""

import os
import time
from collections import defaultdict
import streamlit as st
import config
from rag_engine import RAGEngine

st.set_page_config(
    page_title="AI Agentic RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Custom CSS (Professional Dark Theme) ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

/* Global Reset & Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0d1117;
}

.stApp {
    background: #0d1117;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: #161b22;
}
::-webkit-scrollbar-thumb {
    background: #30363d;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #d4a656;
}

/* ---- HEADER ---- */
.main-header {
    background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
    border-bottom: 1px solid #21262d;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}
.main-header h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.8rem;
    background: linear-gradient(90deg, #f0e4c8, #d4a656, #b8863f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.main-header .status-badge {
    background: #1c2333;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.75rem;
    color: #8b949e;
}
.status-badge .dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #2ea043;
    margin-right: 8px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #21262d !important;
    padding-top: 1rem;
}
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: 'Space Grotesk', sans-serif;
    color: #f0e4c8;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
}
[data-testid="stSidebar"] hr {
    border-color: #21262d;
}

/* Sidebar Stats Card */
.stats-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
}
.stats-card .stat-item {
    text-align: center;
}
.stats-card .stat-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #d4a656;
}
.stats-card .stat-label {
    font-size: 0.65rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

/* Upload box */
[data-testid="stFileUploaderDropzone"] {
    background: #0d1117 !important;
    border: 1.5px dashed #30363d !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #d4a656 !important;
}

/* Buttons in sidebar */
.stButton > button {
    background: linear-gradient(135deg, #d4a656 0%, #b8863f 100%) !important;
    color: #0d1117 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.4rem 1.2rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(212, 166, 86, 0.3);
}

/* Delete buttons (trash) - keep them subtle */
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #8b949e !important;
    padding: 0 8px !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    color: #f85149 !important;
}

/* ---- CHAT AREA ---- */
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1rem 1rem 1rem;
}

/* User Message */
.user-message {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1.2rem;
    animation: fadeIn 0.3s ease;
}
.user-bubble {
    background: linear-gradient(135deg, #1c2333, #2d3548);
    color: #e6edf3;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    border: 1px solid #30363d;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* AI Message */
.ai-message {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 1.2rem;
    animation: fadeIn 0.5s ease;
}
.ai-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #d4a656, #b8863f);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    margin-right: 12px;
    flex-shrink: 0;
}
.ai-bubble {
    background: #161b22;
    color: #e6edf3;
    padding: 14px 20px;
    border-radius: 18px 18px 18px 4px;
    max-width: 80%;
    border: 1px solid #21262d;
    font-size: 0.95rem;
    line-height: 1.6;
}
.ai-bubble .agent-badge {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    padding: 2px 12px;
    border-radius: 20px;
    margin-bottom: 8px;
}

/* Agent Color Themes */
.badge-general { background: #d4a65622; color: #d4a656; border: 1px solid #d4a65644; }
.badge-automation { background: #5b8def22; color: #5b8def; border: 1px solid #5b8def44; }
.badge-extraction { background: #4cc9a022; color: #4cc9a0; border: 1px solid #4cc9a044; }
.badge-analytics { background: #c084fc22; color: #c084fc; border: 1px solid #c084fc44; }

/* Citations chips */
.citation-chip {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 16px;
    padding: 4px 14px;
    display: inline-block;
    font-size: 0.7rem;
    color: #8b949e;
    margin-right: 6px;
    margin-top: 4px;
}
.citation-chip strong {
    color: #d4a656;
}

/* Context expander */
[data-testid="stExpander"] {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 10px;
}
[data-testid="stExpander"] summary {
    color: #8b949e;
    font-size: 0.8rem;
}

/* Welcome message */
.welcome-box {
    text-align: center;
    padding: 4rem 1rem;
}
.welcome-box h2 {
    font-family: 'Space Grotesk', sans-serif;
    color: #f0e4c8;
    font-size: 2rem;
}
.welcome-box p {
    color: #8b949e;
    font-size: 1.1rem;
}

/* Input box - bottom fixed */
.chat-input-container {
    background: #161b22;
    border-top: 1px solid #21262d;
    padding: 1rem 2rem;
    position: sticky;
    bottom: 0;
    z-index: 100;
}
.chat-input-container .stTextInput input {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    color: #e6edf3 !important;
    padding: 0.8rem 1.2rem !important;
    font-size: 1rem !important;
}
.chat-input-container .stTextInput input:focus {
    border-color: #d4a656 !important;
    box-shadow: 0 0 0 2px #d4a65644 !important;
}
.chat-input-container .stButton button {
    background: linear-gradient(135deg, #d4a656 0%, #b8863f 100%) !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Responsive tweaks */
@media (max-width: 768px) {
    .ai-bubble, .user-bubble { max-width: 90%; }
    .main-header h1 { font-size: 1.3rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE INIT ----------------
if "engine" not in st.session_state:
    try:
        st.session_state.engine = RAGEngine()
    except ValueError as e:
        st.error(f"❌ {str(e)}")
        st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

engine = st.session_state.engine

# ---------------- HEADER (Custom HTML) ----------------
st.markdown(f"""
<div class="main-header">
    <h1>🤖 AI Agentic RAG</h1>
    <div class="status-badge">
        <span class="dot"></span>
        {config.GEMINI_MODEL} · {engine.vector_store.backend_name}
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    # --- Stats ---
    docs = engine.get_documents() if hasattr(engine, 'get_documents') else []
    total_docs = len(docs)
    companies = engine.get_all_companies()

    st.markdown(f"""
    <div class="stats-card">
        <div class="stat-item">
            <div class="stat-number">{total_docs}</div>
            <div class="stat-label">Documents</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{len(companies)}</div>
            <div class="stat-label">Companies</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{len(st.session_state.chat_history)}</div>
            <div class="stat-label">Messages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Upload Section ---
    with st.expander("📤 Upload Documents", expanded=True):
        company_name = st.text_input(
            "Company / Client",
            placeholder="e.g. Acme Corp",
            label_visibility="collapsed",
        )
        uploaded_files = st.file_uploader(
            "Choose PDF files", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed"
        )
        if uploaded_files and st.button("🚀 Process PDFs", use_container_width=True):
            if not company_name.strip():
                st.error("Please enter a company name.")
            else:
                with st.spinner("Processing..."):
                    for file in uploaded_files:
                        save_path = os.path.join(config.UPLOAD_DIR, file.name)
                        with open(save_path, "wb") as f:
                            f.write(file.getbuffer())
                        num = engine.ingest_pdf(save_path, company=company_name.strip())
                        st.success(f"✅ {file.name} ({num} chunks)")
                st.rerun()

    # --- Document List ---
    st.markdown("---")
    st.markdown("### 📂 Uploaded Documents")

    if docs:
        # Group by company
        grouped = defaultdict(list)
        for d in docs:
            grouped[d["company"]].append(d)

        for company, company_docs in grouped.items():
            st.markdown(f"**🏢 {company}**")
            for doc in company_docs:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.caption(f"📄 {doc['source']}")
                with col2:
                    # Delete button with popover
                    with st.popover("🗑️", use_container_width=True):
                        st.caption(f"Delete '{doc['source']}'?")
                        if st.button("Yes", key=f"del_{doc['company']}_{doc['source']}"):
                            engine.delete_document(doc["company"], doc["source"])
                            st.success("Deleted!")
                            st.rerun()
        # Delete All
        st.markdown("---")
        with st.popover("🗑️ Delete All", use_container_width=True):
            st.caption("⚠️ Permanently delete ALL documents?")
            if st.button("✅ Yes, Delete All", key="del_all"):
                for d in docs:
                    engine.delete_document(d["company"], d["source"])
                st.success("All deleted!")
                st.rerun()
    else:
        st.info("No documents uploaded.")

    st.markdown("---")

    # --- Settings ---
    st.markdown("### ⚙️ Settings")
    all_companies = engine.get_all_companies()
    selected_company = st.selectbox(
        "🏢 Company Filter",
        options=["All Companies"] + all_companies,
        index=0,
    )
    active_company = None if selected_company == "All Companies" else selected_company

    answer_mode = st.radio(
        "🤖 Answer Mode",
        options=["Single (Fastest)", "Matching", "Compare All"],
        index=0,
        help="Single: AI picks best agent. Matching: keyword match. Compare: all agents answer.",
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.caption(f"🔍 {config.EMBEDDING_MODEL}")

# ---------------- MAIN CHAT AREA ----------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history (chronological order)
if not st.session_state.chat_history:
    st.markdown("""
    <div class="welcome-box">
        <h2>👋 Welcome to AI Agentic RAG</h2>
        <p>Upload your documents and start asking questions.</p>
        <p style="font-size:0.9rem; color:#6e7681;">Powered by Google Gemini + RAG</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for chat in st.session_state.chat_history:
        # --- USER MESSAGE ---
        st.markdown(f"""
        <div class="user-message">
            <div class="user-bubble">🧑 {chat['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        # --- AI RESPONSE ---
        if chat["mode"] == "single":
            agent = chat["agent"].capitalize() if chat["agent"] != "general" else "General"
            color_class = f"badge-{agent.lower()}" if agent.lower() in ["general", "automation", "extraction", "analytics"] else "badge-general"
            st.markdown(f"""
            <div class="ai-message">
                <div class="ai-avatar">🤖</div>
                <div class="ai-bubble">
                    <span class="agent-badge {color_class}">✦ {agent}</span>
                    <div style="margin-top:4px;">{chat['answer']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Multi-agent: show all answers
            st.markdown(f"""
            <div class="ai-message">
                <div class="ai-avatar">🤖</div>
                <div class="ai-bubble" style="width:100%;">
            """, unsafe_allow_html=True)
            for agent_name, answer in chat["answers"].items():
                color_class = f"badge-{agent_name.lower()}" if agent_name.lower() in ["general", "automation", "extraction", "analytics"] else "badge-general"
                st.markdown(f"""
                    <span class="agent-badge {color_class}">✦ {agent_name}</span>
                    <div style="margin-top:4px; margin-bottom:14px;">{answer}</div>
                """, unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

        # --- CITATIONS & CONTEXT (Expandable) ---
        if chat.get("citations"):
            chips = "".join(
                f'<span class="citation-chip">🏢 <strong>{c["company"]}</strong> → {c["source"]}</span>'
                for c in chat["citations"]
            )
            st.markdown(f'<div style="margin: -8px 0 12px 52px;">{chips}</div>', unsafe_allow_html=True)

        with st.expander("📚 View Retrieved Context", expanded=False):
            st.text(chat.get("context", "No context."))

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FIXED INPUT AT BOTTOM ----------------
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)

with st.container():
    col_input, col_btn = st.columns([6, 1])
    with col_input:
        question = st.text_input(
            "Ask a question...",
            placeholder="e.g. What are the leave policies?",
            key="chat_input",
            label_visibility="collapsed",
        )
    with col_btn:
        ask_clicked = st.button("➤ Send", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIC FOR ASKING ----------------
if ask_clicked and question.strip():
    with st.spinner("Thinking..."):
        mode = answer_mode
        if mode == "Single (Fastest)":
            result = engine.ask(question, company=active_company)
            st.session_state.chat_history.append({
                "mode": "single",
                "question": question,
                "answer": result["answer"],
                "agent": result["agent_used"],
                "context": result["context_used"],
                "citations": result.get("citations", []),
            })
        else:
            run_all = (mode == "Compare All")
            result = engine.ask_multi(question, run_all=run_all, company=active_company)
            st.session_state.chat_history.append({
                "mode": "multi",
                "question": question,
                "answers": result["answers"],
                "context": result["context_used"],
                "citations": result.get("citations", []),
            })
    st.rerun()