"""
main.py
-------
Streamlit UI layer. Handles the text box, upload button, and displaying
answers. All the real logic lives in RAGEngine (rag_engine.py).
"""

import os
from collections import defaultdict  # <-- Grouping ke liye
import streamlit as st
import config
from rag_engine import RAGEngine

st.set_page_config(page_title="AI Agentic RAG System", page_icon="📄", layout="wide")

# ---------------- Custom Styling ----------------
AGENT_COLORS = {
    "General": "#d4a656",
    "Automation": "#5b8def",
    "Extraction": "#4cc9a0",
    "Analytics": "#c084fc",
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 15% 0%, #1c2333 0%, #12151f 55%, #0d0f16 100%);
}

/* Title */
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #f0e4c8 0%, #d4a656 60%, #b8863f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 4px;
}

/* Caption under title */
[data-testid="stCaptionContainer"] {
    color: #9aa3b8 !important;
    font-size: 0.95rem !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #161a26;
    border-right: 1px solid #2a3145;
}
[data-testid="stSidebar"] h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f0e4c8 !important;
    font-size: 1.15rem !important;
}

/* Sidebar caption rows (LLM/Embeddings/Vector DB info) */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #7d879c !important;
}

/* File uploader box */
[data-testid="stFileUploaderDropzone"] {
    background: #1d2333 !important;
    border: 1.5px dashed #3a4260 !important;
    border-radius: 12px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #d4a656 0%, #b8863f 100%) !important;
    color: #14161f !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.4rem !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(212, 166, 86, 0.35);
}

/* Text input */
.stTextInput input {
    background: #1a1f2e !important;
    border: 1px solid #2e3652 !important;
    border-radius: 10px !important;
    color: #e8e6e1 !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput input:focus {
    border-color: #d4a656 !important;
    box-shadow: 0 0 0 1px #d4a656 !important;
}

/* Radio (answer mode) */
[data-testid="stSidebar"] .stRadio label {
    color: #c7cede !important;
}

/* Info/warning/success boxes */
[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* Tabs (multi-agent answers) */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: #1a1f2e;
    border-radius: 8px 8px 0 0;
    padding: 8px 18px;
    color: #9aa3b8;
}
.stTabs [aria-selected="true"] {
    background: #262d42 !important;
    color: #f0e4c8 !important;
}

/* Divider */
hr {
    border-color: #232a3d !important;
}

/* Custom Q&A card */
.qa-card {
    background: #171c29;
    border: 1px solid #262d42;
    border-left: 3px solid #d4a656;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 6px;
}
.qa-question {
    color: #f0e4c8;
    font-weight: 600;
    font-size: 1.02rem;
    margin-bottom: 10px;
}
.qa-question span {
    color: #d4a656;
}
.agent-answer {
    background: #1a1f2e;
    border-radius: 8px;
    padding: 14px 16px;
    color: #d8dcea;
    line-height: 1.55;
}
.agent-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.title("📄 AI Agentic RAG System")
st.caption(
    f"Upload PDFs and ask questions about them — powered by **Google {config.GEMINI_MODEL}** "
    "+ RAG + AI Agents"
)

# Initialize RAGEngine only once (reused for the whole session)
if "engine" not in st.session_state:
    try:
        st.session_state.engine = RAGEngine()
    except ValueError as e:
        st.error(str(e))
        st.stop()

engine = st.session_state.engine

# ---------------- Sidebar: Upload + Settings ----------------
with st.sidebar:
    st.header("📤 Upload Documents")

    company_name = st.text_input(
        "Company / Client name",
        placeholder="e.g. Acme Corp",
        help="Tag this upload with a company name so you can later filter "
             "questions to only search within this company's documents.",
    )

    uploaded_files = st.file_uploader(
        "Upload PDF files", type=["pdf"], accept_multiple_files=True
    )

    if uploaded_files and st.button("Process PDFs"):
        if not company_name.strip():
            st.error("Please enter a company name before processing.")
        else:
            with st.spinner("Processing PDFs..."):
                for file in uploaded_files:
                    save_path = os.path.join(config.UPLOAD_DIR, file.name)
                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())
                    num_chunks = engine.ingest_pdf(save_path, company=company_name.strip())
                    st.success(f"{file.name} -> {num_chunks} chunks added under '{company_name.strip()}'")

    # ==============================================================
    # 🔥 UPDATED FEATURE: Grouped Document List + Confirmation Popups
    # ==============================================================
    st.divider()
    st.header("📂 Uploaded Documents")

    # Get list of documents from the engine
    docs = engine.get_documents()

    if docs:
        # Group documents by Company
        grouped_docs = defaultdict(list)
        for doc in docs:
            grouped_docs[doc["company"]].append(doc)

        total = len(docs)
        st.caption(f"Total: {total} document(s)")

        # Show documents grouped by company
        for company, company_docs in grouped_docs.items():
            st.markdown(f"**🏢 {company}**")  # Company heading
            for doc in company_docs:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"📄 {doc['source']}")
                with col2:
                    # 🗑 Delete button with confirmation popover
                    with st.popover("🗑", use_container_width=True):
                        st.caption(f"Delete '{doc['source']}'?")
                        if st.button(
                            "✅ Yes, Delete",
                            key=f"confirm_del_{doc['company']}_{doc['source']}",
                        ):
                            engine.delete_document(doc["company"], doc["source"])
                            st.success(f"Deleted: {doc['source']}")
                            st.rerun()

        # "Delete All" button with confirmation popover
        st.divider()
        with st.popover("🗑️ Delete All Documents", use_container_width=True):
            st.caption("⚠️ Permanently delete ALL uploaded documents?")
            if st.button("✅ Yes, Delete All", key="confirm_del_all"):
                for doc in docs:
                    engine.delete_document(doc["company"], doc["source"])
                st.success("All documents deleted!")
                st.rerun()

    else:
        st.info("No documents uploaded yet.")

    # ==============================================================

    st.divider()
    if engine.vector_store.has_documents():
        st.info("✅ Documents loaded. You can ask questions now.")
    else:
        st.warning("⚠️ No documents uploaded yet.")

    st.divider()
    st.header("🏢 Filter by Company")
    all_companies = engine.get_all_companies()
    company_options = ["All Companies"] + all_companies
    selected_company = st.selectbox(
        "Only answer using documents from:",
        options=company_options,
        help="Choose a specific company to restrict answers to only that "
             "company's uploaded documents. Useful when multiple companies' "
             "PDFs are uploaded at the same time.",
    )
    active_company = None if selected_company == "All Companies" else selected_company

    st.divider()
    st.header("⚙️ Answer Mode")
    answer_mode = st.radio(
        "How should agents answer?",
        options=["Single agent (fastest)", "Matching agents", "Compare all agents"],
        index=0,
        help=(
            "Single agent: Gemini itself reads your question and picks the ONE best-fit "
            "agent (smarter than keyword matching).\n\n"
            "Matching agents: every agent whose keywords match your question answers.\n\n"
            "Compare all agents: Automation, Extraction, Analytics and General RAG "
            "all answer the same question, so you can compare them."
        ),
    )

    st.divider()
    st.caption(f"🧠 LLM: Google {config.GEMINI_MODEL}")
    st.caption(f"🔎 Embeddings: {config.EMBEDDING_MODEL}")
    st.caption(f"🗄️ Storage: {engine.vector_store.backend_name}")

    st.divider()
    if st.button("🗑️ Clear Chat History", key="clear_chat_btn"):
        st.session_state.chat_history = []
        st.rerun()

# ---------------- Main: Chat ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input("Type your question:", placeholder="e.g. How many annual leaves do employees get?")

col1, col2 = st.columns([1, 5])
with col1:
    ask_clicked = st.button("Ask", type="primary")

if ask_clicked and question.strip():
    with st.spinner("Generating answer(s)..."):
        if answer_mode == "Single agent (fastest)":
            result = engine.ask(question, company=active_company)
            st.session_state.chat_history.append(
                {
                    "mode": "single",
                    "question": question,
                    "answer": result["answer"],
                    "agent": result["agent_used"],
                    "context": result["context_used"],
                    "citations": result.get("citations", []),
                    "company": selected_company,
                }
            )
        else:
            run_all = answer_mode == "Compare all agents"
            result = engine.ask_multi(question, run_all=run_all, company=active_company)
            st.session_state.chat_history.append(
                {
                    "mode": "multi",
                    "question": question,
                    "answers": result["answers"],
                    "context": result["context_used"],
                    "citations": result.get("citations", []),
                    "company": selected_company,
                }
            )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- Chat History Display ----------------
for chat in reversed(st.session_state.chat_history):
    st.markdown('<div class="qa-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="qa-question">🧑 <span>Question:</span> {chat["question"]}</div>', unsafe_allow_html=True)
    if chat.get("company"):
        st.markdown(
            f'<div style="color:#6b7488;font-size:0.78rem;margin:-4px 0 10px 4px;">'
            f'🏢 Filtered to: {chat["company"]}</div>',
            unsafe_allow_html=True,
        )

    if chat["mode"] == "single":
        agent_label = chat["agent"].capitalize() if chat["agent"] != "general" else "General"
        color = AGENT_COLORS.get(agent_label, "#d4a656")
        st.markdown(
            f'<span class="agent-badge" style="background:{color}22;color:{color};">🤖 {agent_label} agent</span>'
            f'<span style="color:#6b7488;font-size:0.75rem;margin-left:8px;">'
            f'🧭 chosen by Gemini AI routing (not keyword matching)</span>'
            f'<div class="agent-answer">{chat["answer"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        agent_names = list(chat["answers"].keys())
        tabs = st.tabs([f"🤖 {name}" for name in agent_names])
        for tab, name in zip(tabs, agent_names):
            with tab:
                color = AGENT_COLORS.get(name, "#d4a656")
                st.markdown(
                    f'<span class="agent-badge" style="background:{color}22;color:{color};">{name}</span>'
                    f'<div class="agent-answer">{chat["answers"][name]}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown('</div>', unsafe_allow_html=True)

    if chat.get("citations"):
        chips = "".join(
            f'<span style="background:#1a1f2e;border:1px solid #2e3652;border-radius:20px;'
            f'padding:5px 12px;margin:3px 6px 0 0;display:inline-block;font-size:0.82rem;color:#c7cede;">'
            f'🏢 <b style="color:#d4a656;">{c["company"]}</b> → 📄 {c["source"]}</span>'
            for c in chat["citations"]
        )
        st.markdown(
            f'<div style="margin-top:8px;">{chips}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("📚 View retrieved context"):
        st.text(chat["context"] or "No context found.")
    st.markdown("<br>", unsafe_allow_html=True)