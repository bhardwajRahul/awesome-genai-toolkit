# 🤖 Agentic RAG

> RAG with agent-based reasoning & tool use — self-correcting retrieval systems that think before they answer.

## 📂 Contents

| Notebook | Description | Difficulty |
|----------|-------------|------------|
| *Coming Soon* | Self-correcting retrieval with LangGraph | Advanced |

## 🧠 What You'll Learn

- How to build **CRAG (Corrective RAG)** — detecting and fixing bad retrievals
- Using **LangGraph** to create stateful, multi-step retrieval agents
- **Tool-augmented retrieval** — letting the agent decide when to search
- **Self-RAG** — models that reflect on their own outputs

## 🔥 Why Agentic RAG?

Standard RAG retrieves once and generates. Agentic RAG loops:

```
Query → Retrieve → Grade Docs → (Re-query if needed) → Generate → Self-Check → Answer
```

This makes responses dramatically more accurate for complex questions.

## 🔗 Key Concepts

- **LangGraph** for stateful agent workflows
- **Document Grading** — relevance scoring before generation
- **Query Rewriting** — rephrasing bad queries automatically
- **Corrective RAG (CRAG)** — fallback to web search if docs are insufficient

---

> 🛠️ Prerequisites: Familiar with [Basic RAG](../basic-rag/)? You're ready for this.
