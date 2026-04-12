import streamlit as st
import os
from engine import DocDetectiveEngine
import time

# --- Page Config ---
st.set_page_config(
    page_title="DocDetective | Reasoning RAG",
    page_icon="🧠",
    layout="wide",
)

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .reasoning-box {
        background-color: #1e2129;
        border-left: 4px solid #4CAF50;
        padding: 10px;
        font-size: 0.9em;
        color: #a0a0a0;
        margin-top: 5px;
        border-radius: 5px;
    }
    .highlight {
        color: #4CAF50;
        font-weight: bold;
    }
    h1 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    .sidebar-header {
        font-size: 1.2em;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">🔍 DocDetective v1.1</div>', unsafe_allow_html=True)
    api_key = st.text_input("PageIndex API Key", type="password", help="Get your key from dash.pageindex.ai")
    
    st.divider()
    
    uploaded_file = st.file_uploader("Upload Document (PDF)", type="pdf")
    
    if uploaded_file and api_key:
        if "engine" not in st.session_state or st.session_state.get("file_name") != uploaded_file.name:
            status_placeholder = st.empty()
            with st.spinner("🕵️‍♂️ Detective is processing your document (PageIndex SDK)..."):
                # Save temp file
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    engine = DocDetectiveEngine(api_key)
                    
                    def progress_update(status):
                        status_placeholder.info(f"PageIndex Status: **{status}**")
                    
                    tree = engine.ingest_pdf(temp_path, progress_callback=progress_update)
                    
                    st.session_state.engine = engine
                    st.session_state.tree = tree
                    st.session_state.file_name = uploaded_file.name
                    status_placeholder.success("Indexing complete! PageIndex tree built.")
                except Exception as e:
                    st.error(f"Error during ingestion: {e}")
                
    if "tree" in st.session_state:
        with st.expander("📄 Document Tree (PageIndex)"):
            st.json(st.session_state.tree)

# --- Main App ---
st.title("🧠 DocDetective")
st.markdown("### Reasoning-based PDF Analysis")
st.info("Powered by PageIndex.ai — Using structural tree traversal for zero-hallucination, explainable retrieval.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "reasoning" in message:
            with st.expander("🕵️ Reasoning Process"):
                st.markdown(message["reasoning"])

# Chat Input
if prompt := st.chat_input("Ask anything about the document..."):
    if not api_key:
        st.error("Please provide a PageIndex API Key in the sidebar.")
    elif "engine" not in st.session_state:
        st.error("Please upload a PDF first.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Reasoning over document tree..."):
                try:
                    # Pass history to engine for context-aware chat
                    history = st.session_state.messages[:-1]
                    response = st.session_state.engine.chat(prompt, history=history)
                    
                    full_response = response["answer"]
                    reasoning = response["reasoning"]
                    
                    st.markdown(full_response)
                    with st.expander("🕵️ Reasoning Process"):
                        st.markdown(reasoning)
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": full_response,
                        "reasoning": reasoning
                    })
                except Exception as e:
                    st.error(f"Error during chat: {e}")
