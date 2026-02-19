# RAG Project — Interview Q&A

Use this as a concise, spoken-answer guide. Replace bracketed placeholders with your actual choices.

## 1) Problem Understanding

**Explain your RAG pipeline.**
I built a Retrieval‑Augmented Generation system that answers questions using a private document set. The pipeline embeds documents, retrieves the most relevant chunks for each query, and then prompts the LLM with that context to produce grounded, traceable answers. The goal is to reduce hallucinations and improve factual accuracy on domain‑specific questions.

**Why RAG instead of a plain LLM?**
A plain LLM can only use its pre‑training data and can hallucinate or be outdated. RAG injects fresh, verifiable context from our corpus, so answers are more accurate, source‑grounded, and auditable. It also avoids expensive fine‑tuning for every new document set.

---

## 2) Embeddings & Retrieval

**What embedding model did you use and why?**
I used **[EMBEDDING_MODEL]** because it offers strong semantic retrieval quality, good multilingual coverage (if needed), and predictable latency/cost at scale. It produced stable embeddings that worked well with our domain vocabulary.

**What is chunking and how did you choose chunk size?**
Chunking splits documents into smaller units so retrieval returns focused, relevant context. I used **[CHUNK_SIZE]** tokens with **[OVERLAP]** overlap to balance context granularity and recall. I validated this by testing retrieval precision and answer quality on a small evaluation set.

**What similarity metric did you use?**
I used **[SIMILARITY_METRIC]** (e.g., cosine similarity) because it aligns with how embedding vectors represent semantic closeness. It’s a standard, well‑supported metric in vector databases.

---

## 3) Evaluation & Quality

**How do you evaluate RAG?**
I evaluate both retrieval and generation:
- **Retrieval**: Recall@K, MRR, and qualitative checks to see if the right chunk is retrieved.
- **Generation**: Answer correctness, faithfulness to sources, and citation coverage.
I also run **human spot checks** for high‑impact queries.

**What is hallucination and how does RAG reduce it?**
Hallucination is when the model produces plausible but incorrect content. RAG reduces it by grounding responses in retrieved evidence and prompting the model to only answer using the provided context.

---

## 4) Trade‑offs & Limitations

**What are limitations of your system?**
- Retrieval can miss relevant context if embeddings or chunking are weak.
- Long or complex questions can require multi‑hop reasoning across documents.
- If source docs are outdated or wrong, RAG will still surface those errors.
- Latency increases due to retrieval + generation.

---

## 5) Scalability & Improvements

**How would you scale it?**
I would:
- Use a vector database with efficient ANN search (e.g., HNSW/IVF).
- Batch or cache embeddings for repeat queries.
- Add query routing and caching for common requests.
- Scale retrieval and generation services independently.

**What would you improve?**
- Better chunking (semantic splitting, headings‑aware).
- Hybrid retrieval (BM25 + vector).
- Reranking with a cross‑encoder.
- Improved evaluation harness with gold answers and groundedness scoring.

