# 🕸️ Knowledge Graph RAG

> Graph-based retrieval with citations — structured reasoning over interconnected knowledge.

## 📂 Contents

| Notebook | Description | Difficulty |
|----------|-------------|------------|
| *Coming Soon* | GraphRAG with entity extraction and graph traversal | Advanced |

## 🧠 What You'll Learn

- **GraphRAG** (Microsoft) — building knowledge graphs from documents
- **Entity extraction** and **relationship mapping** with LLMs
- **Graph traversal** for multi-hop reasoning
- Combining graph retrieval with **vector search** for maximum coverage

## 🧩 Why Knowledge Graphs?

Standard RAG retrieves isolated chunks. Knowledge Graphs understand **relationships**:

```
[Apple] --founded_by--> [Steve Jobs]
[Steve Jobs] --also_founded--> [Pixar]
[Pixar] --acquired_by--> [Disney]
```

This enables complex multi-hop questions that chunk-based RAG cannot answer.

## 🔗 Key Concepts

- **GraphRAG** — Microsoft's graph-augmented RAG framework
- **Neo4j / NetworkX** — graph database backends
- **Entity Extraction** — building graph nodes from unstructured text
- **Community Summaries** — global understanding via graph clustering

---

> 🏆 GraphRAG consistently outperforms standard RAG on complex reasoning benchmarks.
