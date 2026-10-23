import streamlit as st
import time
import os
from rag_pipeline import OrientBlackSwanRAG

st.set_page_config(
    page_title="Orient BlackSwan History Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling: Modern Navy-Blue, Slate, White, and Subtle Teal Palette
st.markdown("""
<style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1120px;
    }

    /* Hero Header */
    .app-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        color: #FFFFFF;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
    }
    .app-header h1 {
        font-size: 2.1rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
    }
    .app-header p {
        font-size: 1.05rem;
        color: #94A3B8;
        margin: 0;
        line-height: 1.5;
    }

    /* Badge Pills */
    .status-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 0.3rem 0.75rem;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 9999px;
        background-color: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #E2E8F0;
    }
    .badge-pill.teal {
        background-color: rgba(13, 148, 136, 0.2);
        border-color: rgba(20, 184, 166, 0.4);
        color: #5EEAD4;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .sidebar-card h4 {
        margin: 0 0 0.5rem 0;
        color: #0F172A;
        font-size: 0.95rem;
        font-weight: 600;
    }
    .sidebar-card p, .sidebar-card li {
        color: #475569;
        font-size: 0.85rem;
        line-height: 1.45;
    }

    /* Suggested Question Buttons */
    .suggestions-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    div[data-testid="stButton"] button {
        background-color: #FFFFFF;
        color: #1E293B;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 0.55rem 0.9rem;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.15s ease-in-out;
        text-align: left;
        width: 100%;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }
    div[data-testid="stButton"] button:hover {
        border-color: #0D9488;
        color: #0F766E;
        background-color: #F0FDFA;
        box-shadow: 0 2px 4px -1px rgba(13, 148, 136, 0.1);
    }

    /* Evidence & Source Citation Card */
    .evidence-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #0D9488;
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        margin-top: 0.75rem;
    }
    .evidence-card.unsupported {
        border-left-color: #94A3B8;
        background: #F1F5F9;
    }
    .evidence-tag {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        margin-bottom: 0.45rem;
    }
    .evidence-tag.grounded {
        background-color: #CCFBF1;
        color: #0F766E;
    }
    .evidence-tag.out-of-scope {
        background-color: #E2E8F0;
        color: #475569;
    }
    .citation-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.25rem;
    }
    .citation-body {
        font-size: 0.85rem;
        color: #475569;
        line-height: 1.5;
        font-style: italic;
    }

    /* Empty state card */
    .empty-state {
        background: #FFFFFF;
        border: 1px dashed #CBD5E1;
        border-radius: 10px;
        padding: 2.2rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    .empty-state h3 {
        color: #1E293B;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .empty-state p {
        color: #64748B;
        font-size: 0.9rem;
        max-width: 540px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG Pipeline
@st.cache_resource
def get_rag_pipeline():
    return OrientBlackSwanRAG()

rag = get_rag_pipeline()
count = rag.collection.count()

# Sidebar: Context, Meta, Guidance
with st.sidebar:
    st.markdown("### 🏛️ Research Assistant")
    st.caption("GenAI Mid-Term Project 4 • Academic Submission")
    
    st.markdown("""
    <div class="sidebar-card">
        <h4>📄 Catalogue Source</h4>
        <ul style="padding-left: 1.2rem; margin: 0;">
            <li><strong>Title:</strong> History Catalogue 2024–25</li>
            <li><strong>Publisher:</strong> Orient BlackSwan</li>
            <li><strong>Extent:</strong> 91 Physical Pages</li>
            <li><strong>Status:</strong> <span style="color:#0D9488; font-weight:600;">Verified & Grounded</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-card">
        <h4>⚡ Vector Database</h4>
        <ul style="padding-left: 1.2rem; margin: 0;">
            <li><strong>Engine:</strong> ChromaDB Persistent</li>
            <li><strong>Embedding:</strong> all-MiniLM-L6-v2 (ONNX)</li>
            <li><strong>Indexed Chunks:</strong> {count} Chunks</li>
            <li><strong>Local / API Keys:</strong> 100% Offline (Zero API cost)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <h4>💡 System Scope & Guardrails</h4>
        <p style="margin: 0;">
            Answers are restricted solely to the provided history catalogue. Queries regarding other academic disciplines, ungrounded external trivia, or subjective rankings return safe, document-grounded responses.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Hero Header
st.markdown(f"""
<div class="app-header">
    <h1>Orient BlackSwan History Assistant</h1>
    <p>Explore the History Catalogue 2024–25 with evidence-grounded answers and physical PDF citations.</p>
    <div class="status-bar">
        <span class="badge-pill teal">● Vector Store: {count} Chunks Active</span>
        <span class="badge-pill">🛡️ Strict Evidence Validation</span>
        <span class="badge-pill">📌 Exact Page Citations</span>
        <span class="badge-pill">🔒 Document-Grounded Only</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Suggested Questions Grid
st.markdown('<div class="suggestions-label">💡 Suggested Catalogue Questions</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

example_selected = None

with col1:
    if st.button("1. On what date were prices last updated?", use_container_width=True):
        example_selected = "On what date were the prices in this catalogue last updated?"
with col2:
    if st.button("2. In which year was Orient BlackSwan incorporated?", use_container_width=True):
        example_selected = "In which year was Orient BlackSwan incorporated?"
with col3:
    if st.button("3. Price of a Physics textbook?", use_container_width=True):
        example_selected = "What is the price of a Physics textbook?"
with col4:
    if st.button("4. Current Minister of Education?", use_container_width=True):
        example_selected = "Who is the current Minister of Education?"
with col5:
    if st.button("5. Suitable history books for a beginner?", use_container_width=True):
        example_selected = "Which history books could be suitable for a beginner?"

# Render Chat History or Empty State
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <h3>Ready to Explore the Catalogue</h3>
        <p>Click any suggested question above or type your inquiry in the search bar below to retrieve catalogue information with real citations.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "metadata" in message and message["metadata"]:
                meta = message["metadata"]
                if meta.get("page"):
                    st.markdown(f"""
                    <div class="evidence-card">
                        <span class="evidence-tag grounded">Verified Catalogue Evidence</span>
                        <div class="citation-title">Source Reference: Physical PDF Page {meta['page']}</div>
                        <div class="citation-body">"{meta['excerpt']}"</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="evidence-card unsupported">
                        <span class="evidence-tag out-of-scope">Out of Catalogue Scope</span>
                        <div class="citation-title">Verification Finding</div>
                        <div class="citation-body">{meta.get('excerpt', 'No direct evidence found in the catalogue.')}</div>
                    </div>
                    """, unsafe_allow_html=True)

# Chat Input & Interaction
user_query = st.chat_input("Ask a question about books, publishers, or dates in the History Catalogue...")

if example_selected:
    user_query = example_selected

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Searching catalogue vector store & validating evidence..."):
            result = rag.answer_question(user_query)
            time.sleep(0.2)
            
            answer_text = result["answer"]
            st.markdown(f"**Answer:** {answer_text}")
            
            meta_info = {
                "page": result.get("page"),
                "excerpt": result.get("excerpt")
            }
            
            if result.get("page"):
                st.markdown(f"""
                <div class="evidence-card">
                    <span class="evidence-tag grounded">Verified Catalogue Evidence</span>
                    <div class="citation-title">Source Reference: Physical PDF Page {result['page']}</div>
                    <div class="citation-body">"{result['excerpt']}"</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="evidence-card unsupported">
                    <span class="evidence-tag out-of-scope">Out of Catalogue Scope</span>
                    <div class="citation-title">Verification Finding</div>
                    <div class="citation-body">{result.get('excerpt', 'No direct evidence found in the catalogue.')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"**Answer:** {answer_text}",
            "metadata": meta_info
        })
