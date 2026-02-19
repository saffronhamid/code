# Project Documentation: Agentic RAG-Based Question Answering System

## Overview
This project implements an agentic Retrieval-Augmented Generation (RAG) system that answers questions using both a local document corpus and Wikipedia. It ingests documents from URLs and local files, embeds them into a FAISS vector store, and uses a LangGraph workflow with a ReAct agent to decide whether to retrieve from the local store or query Wikipedia.

Primary entry points:
- CLI: `main.py`
- Web UI: `streamlit_app.py`

## Key Features
- Document ingestion from URLs, PDFs, TXTs, and directories
- Chunking with overlap for better retrieval
- OpenAI embeddings + FAISS vector storage
- LangGraph workflow orchestration
- ReAct agent with tool selection (local retriever or Wikipedia)
- Dual interfaces: CLI and Streamlit UI

## Architecture
High-level flow:
1. Ingest documents from configured sources.
2. Split documents into chunks.
3. Embed chunks and store in FAISS.
4. On query:
   - Retrieve relevant chunks.
   - Use ReAct agent to pick a tool (retriever or Wikipedia).
   - Generate final answer.

## Project Structure
```
data/                           # Data sources (PDF/TXT files)
src/
  config/                       # Configuration and model setup
  document_ingestion/           # Loading and splitting documents
  graph_builder/                # LangGraph workflow construction
  node/                         # RAG nodes and ReAct agent
  state/                        # LangGraph state model
  vectorstore/                  # FAISS vector store logic
main.py                         # CLI entry point
streamlit_app.py                # Streamlit UI entry point
requirements.txt                # Python dependencies
README.md                       # Repository overview
.env                            # Environment variables (API keys)
```

## Core Modules

### Configuration
`src/config/config.py`
- Loads `.env` and `OPENAI_API_KEY`
- Sets model and chunking parameters
- Defines default sources

### Document Ingestion
`src/document_ingestion/document_processor.py`
- Loads data from URLs, PDF, TXT, and directories
- Splits into chunks using `RecursiveCharacterTextSplitter`

### Vector Store
`src/vectorstore/vectorstore.py`
- Uses `OpenAIEmbeddings` to embed chunks
- Stores embeddings in FAISS and exposes a retriever

### Graph Workflow
`src/graph_builder/graph_builder.py`
- Builds a LangGraph pipeline:
  - `retriever` node (fetch documents)
  - `responder` node (generate answer)

### ReAct Agent Node
`src/node/reactnode.py`
- Builds tools:
  - `retriever`: local vector store
  - `wikipedia`: general knowledge lookup
- Creates a ReAct agent that selects the appropriate tool

### State Model
`src/state/rag_state.py`
- Defines the RAG workflow state (`question`, `retrieved_docs`, `answer`)

## How It Works

### Initialization
- Sources are loaded from `data/sources.txt`, `data/urls.txt`, or `data/url.txt`
- Documents are processed and split
- Embeddings are generated and stored in FAISS

### Query Time
- User query enters the LangGraph pipeline
- Retriever fetches relevant docs
- ReAct agent decides:
  - Use local retriever for corpus-based questions
  - Use Wikipedia for general knowledge
- Final answer returned

## Interfaces

### CLI
Run:
```bash
python main.py
```
The script runs example questions, then optionally enters interactive mode.

### Streamlit UI
Run:
```bash
streamlit run streamlit_app.py
```
You can edit sources, upload PDFs/TXTs, and search interactively.

## Configuration and Environment
- Requires `OPENAI_API_KEY` in `.env`
- Default sources include two URLs and the `data/` directory
- Model default: `openai:gpt-4o`

## Limitations
- Vector store is rebuilt each run (no persistence)
- Wikipedia tool requires internet access
- No explicit citations included in final answers

## Suggested Next Improvements
- Persist FAISS index to disk for faster startup
- Add citation tracing for answers
- Add tests for ingestion, retrieval, and agent routing
- Consolidate legacy node logic with agent-based nodes
