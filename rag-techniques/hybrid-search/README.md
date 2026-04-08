# 🔍 Hybrid Search RAG

> Combining vector + keyword search for best-of-both-worlds retrieval accuracy.

## 📂 Contents

| Notebook | Description | Difficulty |
|----------|-------------|------------|
| *Coming Soon* | Combine vector + keyword search (BM25) | Intermediate |

## 🧠 What You'll Learn

- Why **pure vector search fails** for exact keyword lookups (names, codes, IDs)
- Implementing **BM25** sparse retrieval alongside dense embeddings
- **Reciprocal Rank Fusion (RRF)** — merging rankings from multiple retrievers
- Using **Weaviate / Elasticsearch** for production hybrid search

## ⚖️ Vector vs Keyword vs Hybrid

| Method | Strength | Weakness |
|--------|----------|----------|
| Vector Search | Semantic similarity | Misses exact terms |
| BM25 Keyword | Exact term matching | No semantic understanding |
| **Hybrid** | **Both** | Slightly more complex |

## 🚀 Quick Start

```bash
pip install rank_bm25 sentence-transformers
```

## 🔗 Key Concepts

- **BM25** — probabilistic keyword ranking
- **Dense Retrieval** — embedding-based semantic search
- **Re-ranking** — cross-encoder models for final ordering
- **Reciprocal Rank Fusion** — score fusion without normalization

---

> 💡 Hybrid search typically outperforms pure vector search by 10–20% on real-world benchmarks.
