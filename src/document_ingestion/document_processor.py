"""Document processing module for loading and splitting documents."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Union

from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    """Handles document loading and processing"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize document processor
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_from_url(self, url: str) -> List[Document]:
        """Load document(s) from a URL."""
        loader = WebBaseLoader(url)
        return loader.load()

    def load_from_pdf(self, file_path: Union[str, Path]) -> List[Document]:
        """Load document(s) from a PDF file."""
        loader = PyPDFLoader(str(file_path))
        return loader.load()

    def load_from_txt(self, file_path: Union[str, Path]) -> List[Document]:
        """Load document(s) from a TXT file."""
        loader = TextLoader(str(file_path), encoding="utf-8")
        return loader.load()

    def _iter_files(self, directory: Path, patterns: Iterable[str]) -> Iterable[Path]:
        for pattern in patterns:
            yield from directory.rglob(pattern)
    
    def load_documents(self, sources: List[str]) -> List[Document]:
        """
        Load documents from URLs, PDF directories, or TXT files

        Args:
            sources: List of URLs, PDF folder paths, or TXT file paths

        Returns:
            List of loaded documents
        """
        docs: List[Document] = []

        for src in sources:
            src = src.strip()
            if not src or src.startswith("#"):
                continue

            if src.startswith("http://") or src.startswith("https://"):
                docs.extend(self.load_from_url(src))
                continue

            path = Path(src)
            if path.is_dir():
                for pdf in self._iter_files(path, ["*.pdf"]):
                    docs.extend(self.load_from_pdf(pdf))
                for txt in self._iter_files(path, ["*.txt"]):
                    docs.extend(self.load_from_txt(txt))
                continue

            if path.is_file():
                suffix = path.suffix.lower()
                if suffix == ".pdf":
                    docs.extend(self.load_from_pdf(path))
                elif suffix == ".txt":
                    docs.extend(self.load_from_txt(path))
                else:
                    raise ValueError(f"Unsupported file type: {path}")
                continue

            raise FileNotFoundError(f"Source not found: {src}")

        return docs
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of split documents
        """
        return self.splitter.split_documents(documents)
    
    def process_sources(self, sources: List[str]) -> List[Document]:
        """
        Complete pipeline to load and split documents
        
        Args:
            sources: List of sources (URLs, directories, or files) to process
            
        Returns:
            List of processed document chunks
        """
        docs = self.load_documents(sources)
        return self.split_documents(docs)

    def process_urls(self, urls: List[str]) -> List[Document]:
        """Backward-compatible alias for older call sites."""
        return self.process_sources(urls)
