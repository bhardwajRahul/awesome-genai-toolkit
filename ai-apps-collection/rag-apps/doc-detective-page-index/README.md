# 🧠 DocDetective — Reasoning RAG Chat for PDFs

[![PageIndex](https://img.shields.io/badge/Powered%20By-PageIndex.ai-4CAF50?style=for-the-badge)](https://pageindex.ai)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge)](https://streamlit.io)

**DocDetective** is a "vectorless" Reasoning RAG application designed to chat with complex PDFs (financial reports, legal documents, research papers) using true hierarchical document analysis. Unlike traditional fuzzy vector search, DocDetective builds a structural tree of your document to understand context like a human expert.

---

## ✨ Features

- **🔍 True Reasoning Retrieval**: Uses structural tree traversal (powered by **PageIndex**) for zero-hallucination, explainable retrieval.
- **📄 PageIndex Visualization**: Explore the hierarchical "Document Tree" generated for your PDF.
- **🕵️ Explainable AI**: Every answer comes with a "Reasoning Process" breakdown showing exactly how the AI navigated your document.
- **🎨 Premium UI**: A sleek, dark-themed Streamlit interface optimized for document analysis.
- **⚡ Real-time Feedback**: Live status updates during document ingestion (initializing, indexing, completed).

---

## 🛠️ Technology Stack

- **[PageIndex SDK](https://docs.pageindex.ai)**: Core engine for hierarchical indexing and agentic RAG.
- **Streamlit**: Modern frontend interface.
- **PyMuPDF**: Robust PDF processing.
- **Gemini 1.5 Pro/Flash**: The intelligence behind the reasoning.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- A **PageIndex API Key** from the [Developer Dashboard](https://dash.pageindex.ai).

### 2. Installation
```bash
# Clone the repository (if downloading separately)
git clone https://github.com/shubh-vedi/doc-detective
cd doc-detective-page-index

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment
Create a `.env` file in the root directory:
```env
PAGEINDEX_API_KEY=your_api_key_here
GOOGLE_API_KEY=your_gemini_key_here
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## 📖 How It Works

1. **Upload**: Drag and drop any complex PDF.
2. **Indexing**: PageIndex builds a hierarchical tree of chapters and sections.
3. **Reasoning**: When you ask a question, the agent traverses the tree nodes to find the exact pages relevant to your query.
4. **Answer**: The AI synthesizes an answer with citations and explains its retrieval logic.

---

## 📜 License
Licensed under the [MIT License](LICENSE).

---

Built with ❤️ by [Shubham Vedi](https://github.com/shubh-vedi)
