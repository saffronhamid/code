# 🔍 RAG-Based Question Answering System

A Retrieval-Augmented Generation (RAG) application built using **LangChain**, **FAISS**, **OpenAI**, and **Streamlit**.  
This project ingests unstructured text, indexes it with vector embeddings, and provides accurate, context-aware answers to user queries.

---

## 🚀 Features

- 📄 Document loading & text preprocessing  
- 🧠 Embedding generation using OpenAI  
- 🗂️ Vector storage using FAISS  
- 🔎 Relevant-chunk retrieval with LangChain  
- 🤖 Response generation using OpenAI LLMs  
- 🌐 Simple and interactive Streamlit UI  
- 🔧 Modular & MLOps-friendly design  

---

## 🧱 Architecture Overview

```mermaid
flowchart TD
    A[User Query] --> B[Streamlit UI]
    B --> C[Retriever - FAISS Vector Store]
    C --> D[Relevant Documents]
    D --> E[LangChain RAG Pipeline]
    E --> F[OpenAI LLM]
    F --> G[Final Answer]
