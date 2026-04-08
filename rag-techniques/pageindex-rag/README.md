# PageIndex RAG — Vectorless, Reasoning-Based Retrieval

> **No Vector DB. No Chunking. No Similarity Search.** PageIndex uses LLM reasoning over a hierarchical tree index to retrieve exactly the right pages — the way a human expert would.

[![Stars](https://img.shields.io/github/stars/VectifyAI/PageIndex?style=social)](https://github.com/VectifyAI/PageIndex)

## Contents

| Notebook | Description | Difficulty |
|----------|-------------|------------|
| [pageindex_rag_complete_guide.ipynb](./pageindex_rag_complete_guide.ipynb) | PageIndex Cloud API: Index PDF, tree search, reasoning-based retrieval, Chat API | Beginner |

## What is PageIndex?

Traditional vector RAG: **embed → chunk → similarity search** — retrieves *similar* text, not *relevant* text.

PageIndex: **build tree index → LLM reasons over it → fetch exact pages** — retrieves *relevant* context like a human expert.

```
Your PDF
   ↓
[PageIndex Tree]
├── Section 1 (pages 1-5)    ← LLM reasons: "relevant to query?"
│   ├── Sub-section 1.1
│   └── Sub-section 1.2
├── Section 2 (pages 6-12)   ← LLM reasons: "not relevant, skip"
└── Section 3 (pages 13-20)  ← LLM reasons: "highly relevant!"
         ↓
   Fetch pages 13-20
         ↓
   Generate Answer
```

## Key Advantages

| Feature | Vector RAG | PageIndex RAG |
|---------|-----------|---------------|
| Retrieval method | Cosine similarity | LLM reasoning |
| Chunking required | Yes | No |
| Vector DB required | Yes | No |
| Explainability | Low (black box) | High (traceable) |
| Multi-hop reasoning | Hard | Native |
| Long documents | Struggles | Excels |
| FinanceBench accuracy | ~80% | **98.7%** |

## Quick Start

```bash
pip install pageindex openai
```

```python
from pageindex import PageIndexClient

pi_client = PageIndexClient(api_key="YOUR_PAGEINDEX_API_KEY")
doc_id = pi_client.submit_document("your_document.pdf")["doc_id"]

# Use Chat API for instant Q&A
for chunk in pi_client.chat_completions(
    messages=[{"role": "user", "content": "What are the key findings?"}],
    doc_id=doc_id,
    stream=True,
):
    print(chunk, end="", flush=True)
```

## Notebook Sections

1. **Setup** — Install deps, configure PageIndex & OpenAI API keys
2. **Index a PDF** — Submit document to PageIndex Cloud
3. **Explore the Tree** — View hierarchical structure (no embeddings!)
4. **Reasoning-Based Retrieval** — LLM tree search with full reasoning trace
5. **Answer Generation** — Grounded answers from retrieved context
6. **Reusable Pipeline** — Wrapped into a clean function for multiple queries
7. **Chat API** — One-liner Q&A with streaming responses
8. **Try Your Own PDF** — Plug in any document

---

> Source: [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex) | [Docs](https://docs.pageindex.ai) | [Dashboard](https://dash.pageindex.ai)
