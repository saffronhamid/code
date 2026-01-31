"""Streamlit UI for Agentic RAG System - Simplified Version"""

import streamlit as st
from pathlib import Path
import sys
import time
import tempfile
from typing import List

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.config.config import Config
from src.document_ingestion.document_processor import DocumentProcessor
from src.vectorstore.vectorstore import VectorStore
from src.graph_builder.graph_builder import GraphBuilder

# Page configuration
st.set_page_config(
    page_title="🤖 RAG Search",
    page_icon="🔍",
    layout="centered"
)

# Simple CSS
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if "sources_key" not in st.session_state:
        st.session_state.sources_key = None
    if 'history' not in st.session_state:
        st.session_state.history = []

@st.cache_resource
def initialize_rag(sources_key: tuple[str, ...]):
    """Initialize the RAG system (cached)"""
    try:
        # Initialize components
        llm = Config.get_llm()
        doc_processor = DocumentProcessor(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        vector_store = VectorStore()

        if not sources_key:
            raise ValueError("No sources provided.")

        # Process documents
        documents = doc_processor.process_sources(list(sources_key))
        
        # Create vector store
        vector_store.create_vectorstore(documents)
        
        # Build graph
        graph_builder = GraphBuilder(
            retriever=vector_store.get_retriever(),
            llm=llm
        )
        graph_builder.build()
        
        return graph_builder, len(documents)
    except Exception as e:
        st.error(f"Failed to initialize: {str(e)}")
        return None, 0

def _parse_sources(text: str) -> List[str]:
    sources: List[str] = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        sources.append(line)
    return sources

def _save_upload_to_temp(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix or ".bin"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name

def main():
    """Main application"""
    init_session_state()
    
    # Title
    st.title("🔍 RAG Document Search")
    st.markdown("Ask questions about the loaded documents")

    with st.sidebar:
        st.markdown("### Sources")
        st.caption("One per line: URL, local file path, or directory path.")
        default_sources = "\n".join(Config.DEFAULT_SOURCES)
        sources_text = st.text_area(
            "Sources list",
            value=default_sources,
            height=160,
            label_visibility="collapsed",
        )
        uploads = st.file_uploader(
            "Upload PDFs/TXTs",
            type=["pdf", "txt"],
            accept_multiple_files=True,
        )

    sources = _parse_sources(sources_text)
    for up in uploads or []:
        sources.append(_save_upload_to_temp(up))

    sources_key = tuple(sources)
    if st.session_state.sources_key != sources_key:
        st.session_state.sources_key = sources_key
        st.session_state.initialized = False
        st.session_state.rag_system = None

    # Initialize system
    if not st.session_state.initialized:
        with st.spinner("Loading system..."):
            rag_system, num_chunks = initialize_rag(sources_key)
            if rag_system:
                st.session_state.rag_system = rag_system
                st.session_state.initialized = True
                st.success(f"✅ System ready! ({num_chunks} document chunks loaded)")
    
    st.markdown("---")
    
    # Search interface
    with st.form("search_form"):
        question = st.text_input(
            "Enter your question:",
            placeholder="What would you like to know?"
        )
        submit = st.form_submit_button("🔍 Search")
    
    # Process search
    if submit and question:
        if st.session_state.rag_system:
            with st.spinner("Searching..."):
                start_time = time.time()
                
                # Get answer
                result = st.session_state.rag_system.run(question)
                
                elapsed_time = time.time() - start_time
                
                # Add to history
                st.session_state.history.append({
                    'question': question,
                    'answer': result['answer'],
                    'time': elapsed_time
                })
                
                # Display answer
                st.markdown("### 💡 Answer")
                st.success(result['answer'])
                
                # Show retrieved docs in expander
                with st.expander("📄 Source Documents"):
                    for i, doc in enumerate(result['retrieved_docs'], 1):
                        st.text_area(
                            f"Document {i}",
                            doc.page_content[:300] + "...",
                            height=100,
                            disabled=True
                        )
                
                st.caption(f"⏱️ Response time: {elapsed_time:.2f} seconds")
    
    # Show history
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 📜 Recent Searches")
        
        for item in reversed(st.session_state.history[-3:]):  # Show last 3
            with st.container():
                st.markdown(f"**Q:** {item['question']}")
                st.markdown(f"**A:** {item['answer'][:200]}...")
                st.caption(f"Time: {item['time']:.2f}s")
                st.markdown("")

if __name__ == "__main__":
    main()
