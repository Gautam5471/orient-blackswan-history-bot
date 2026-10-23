import streamlit as st
import time
import os
from rag_pipeline import OrientBlackSwanRAG

st.set_page_config(
    page_title="Orient BlackSwan History Bot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished typography, badges, and layout
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 9999px;
        background-color: #E2E8F0;
        color: #334155;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .source-box {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 0.8rem 1rem;
        border-radius: 0.375rem;
        margin-top: 0.6rem;
        font-size: 0.9rem;
    }
    .not-found-badge {
        display: inline-block;
        background-color: #FEE2E2;
        color: #991B1B;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
    }
    .found-badge {
        display: inline-block;
        background-color: #DCFCE7;
        color: #166534;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG Pipeline in session state
@st.cache_resource
def get_rag_pipeline():
    return OrientBlackSwanRAG()

rag = get_rag_pipeline()

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/feathericons/feather/master/icons/book-open.svg", width=48)
    st.title("Project Details")
    st.markdown("**Mid-Term Project 4**")
    st.markdown("Orient BlackSwan History Bot")
    
    st.divider()
    st.subheader("🛠️ Technology Stack")
    st.markdown("""
    - **Language:** Python 3.10+
    - **Vector Database:** ChromaDB
    - **Embeddings:** all-MiniLM-L6-v2 (ONNX)
    - **Framework:** Streamlit + PyPDF
    - **Index State:** 837 Chunks (Persistent)
    """)
    
    st.divider()
    st.subheader("📄 Document Source")
    st.markdown("""
    - **File:** `data/History_2024-25.pdf`
    - **Pages:** 91 Physical Pages
    - **Subject:** History Catalogue 2024–25
    """)

    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Header
st.markdown('<div class="main-header">Orient BlackSwan History Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">An AI-powered RAG assistant for the Orient BlackSwan History Catalogue 2024–25.</div>', unsafe_allow_html=True)

# Status pill
count = rag.collection.count()
st.markdown(f'<span class="badge-pill">✅ Index Active: {count} Chunks</span><span class="badge-pill">🛡️ Strict Evidence Validation</span><span class="badge-pill">📌 Exact Source Citations</span>', unsafe_allow_html=True)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Example Questions Section
st.markdown("### 💡 Mandatory Assignment Questions")
col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

example_selected = None

with col1:
    if st.button("Q1: Date prices updated?", use_container_width=True):
        example_selected = "On what date were the prices in this catalogue last updated?"
with col2:
    if st.button("Q2: Year incorporated?", use_container_width=True):
        example_selected = "In which year was the publisher (Orient BlackSwan) incorporated?"
with col3:
    if st.button("Q3: Physics textbook price?", use_container_width=True):
        example_selected = "What is the price of a Physics textbook?"
with col4:
    if st.button("Q4: Current Minister of Education?", use_container_width=True):
        example_selected = "Who is the current Minister of Education?"
with col5:
    if st.button("Q5: Best history book for beginners?", use_container_width=True):
        example_selected = "Which is the \"best\" history book for a beginner?"

# Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "metadata" in message and message["metadata"]:
            meta = message["metadata"]
            if meta.get("page"):
                st.markdown(f"""
                <div class="source-box">
                    <span class="found-badge">GROUNDED EVIDENCE</span><br>
                    <strong>Source Citation:</strong> Physical PDF Page {meta['page']}<br>
                    <strong>Excerpt:</strong> <em>"{meta['excerpt']}"</em>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="source-box">
                    <span class="not-found-badge">UNSUPPORTED / OUT OF SCOPE</span><br>
                    <strong>Reasoning:</strong> {meta.get('excerpt', 'No direct evidence found in catalogue.')}
                </div>
                """, unsafe_allow_html=True)

# Handle Question Submission
user_query = st.chat_input("Ask a question about the Orient BlackSwan History Catalogue...")

# If an example button was clicked, treat it as input
if example_selected:
    user_query = example_selected

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Searching catalogue vector index and verifying evidence..."):
            result = rag.answer_question(user_query)
            time.sleep(0.3)  # smooth UI feel
            
            answer_text = result["answer"]
            st.markdown(f"**Answer:** {answer_text}")
            
            meta_info = {
                "page": result.get("page"),
                "excerpt": result.get("excerpt")
            }
            
            if result.get("page"):
                st.markdown(f"""
                <div class="source-box">
                    <span class="found-badge">GROUNDED EVIDENCE</span><br>
                    <strong>Source Citation:</strong> Physical PDF Page {result['page']}<br>
                    <strong>Excerpt:</strong> <em>"{result['excerpt']}"</em>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="source-box">
                    <span class="not-found-badge">UNSUPPORTED / OUT OF SCOPE</span><br>
                    <strong>Reasoning:</strong> {result.get('excerpt', 'No direct evidence in catalogue.')}
                </div>
                """, unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"**Answer:** {answer_text}",
            "metadata": meta_info
        })
