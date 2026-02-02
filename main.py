"""Main application entry point for Agentic RAG system"""

import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.config.config import Config
from src.document_ingestion.document_processor import DocumentProcessor
from src.vectorstore.vectorstore import VectorStore
from src.graph_builder.graph_builder import GraphBuilder

class AgenticRAG:
    """Main Agentic RAG application"""
    
    def __init__(self, sources=None, urls=None):
        """
        Initialize Agentic RAG system
        
        Args:
            sources: List of sources (URLs, files, or directories) to process (uses defaults if None)
            urls: Backward-compatible alias for sources (URLs only)
        """
        print("🚀 Initializing Agentic RAG System...")
        
        # Use default sources if none provided
        self.sources = sources or urls or Config.DEFAULT_SOURCES
        self.urls = self.sources
        
        # Initialize components
        self.llm = Config.get_llm()
        self.doc_processor = DocumentProcessor(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        self.vector_store = VectorStore()
        
        # Process documents and create vector store
        self._setup_vectorstore()
        
        # Build graph
        self.graph_builder = GraphBuilder(
            retriever=self.vector_store.get_retriever(),
            llm=self.llm
        )
        self.graph_builder.build()
        
        print("✅ System initialized successfully!\n")
    
    def _setup_vectorstore(self):
        """Setup vector store with processed documents"""
        print(f"📄 Processing {len(self.urls)} URLs...")
        documents = self.doc_processor.process_urls(self.urls)
        print(f"📊 Created {len(documents)} document chunks")
        
        print("🔍 Creating vector store...")
        self.vector_store.create_vectorstore(documents)
    
    def ask(self, question: str) -> str:
        """
        Ask a question to the RAG system
        
        Args:
            question: User question
            
        Returns:
            Generated answer
        """
        print(f"❓ Question: {question}\n")
        print("🤔 Processing...")
        
        result = self.graph_builder.run(question)
        answer = result['answer']
        
        print(f"✅ Answer: {answer}\n")
        return answer
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("💬 Interactive Mode - Type 'quit' to exit\n")
        
        while True:
            question = input("Enter your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if question:
                self.ask(question)
                print("-" * 80 + "\n")

def main():
    """Main function"""
    sources_file_candidates = [
        Path("data/sources.txt"),
        Path("data/urls.txt"),
        Path("data/url.txt"),
    ]
    sources = None

    for candidate in sources_file_candidates:
        if candidate.exists():
            with open(candidate, "r", encoding="utf-8") as f:
                sources = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.strip().startswith("#")
                ]
            break
    
    # Initialize RAG
    rag = AgenticRAG(sources=sources)
    
    # Example questions
    example_questions = [
        "What is the concept of agent loop in autonomous agents?",
        "What are the key components of LLM-powered agents?",
        "Explain the concept of diffusion models for video generation."
    ]
    
    print("=" * 80)
    print("📝 Running example questions:")
    print("=" * 80 + "\n")
    for question in example_questions:
        rag.ask(question)
        print("=" * 80 + "\n")
    
    print("\n" + "=" * 80)
    user_input = input("Would you like to enter the most developed interactive mode? (y/n): ")
    if user_input.lower() == 'y':
        rag.interactive_mode()

if __name__ == "__main__":
    main()
