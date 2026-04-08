# 🔵 Basic RAG

> Simple retrieval + generation pipelines — the foundation of every production RAG system.

## 📂 Contents

| Notebook | Description | Difficulty |
|----------|-------------|------------|
| [build_rag_from_scratch.ipynb](./build_rag_from_scratch.ipynb) | Chat with your PDF using OpenAI + ChromaDB — no frameworks, ~50 lines of core logic | Beginner |

## 🧠 What You'll Learn

- How to **chunk and embed** documents into a vector store
- How to **retrieve** the most relevant chunks for a query
- How to **augment** an LLM prompt with retrieved context
- End-to-end RAG pipeline with **ChromaDB** + **OpenAI**

## 🚀 Quick Start

```bash
pip install -r requirements.txt
jupyter notebook build_rag_from_scratch.ipynb
```

## 🔗 Key Concepts

- **Chunking** — splitting documents into manageable pieces
- **Embedding** — converting text to semantic vectors
- **Vector Search** — finding similar chunks via cosine similarity
- **Prompt Augmentation** — injecting context into the LLM prompt

---

> 💡 New to RAG? Start here before exploring [Agentic RAG](../agentic-rag/) or [Hybrid Search](../hybrid-search/).
