from pageindex import PageIndexClient
import json
import time
from typing import List, Dict, Any, Optional

class DocDetectiveEngine:
    def __init__(self, api_key: str):
        self.api_key = api_key.strip()
        self.client = PageIndexClient(api_key=self.api_key)
        self.doc_id = None
        self.tree = {}

    def ingest_pdf(self, pdf_path: str, progress_callback=None):
        """
        Uploads PDF to PageIndex and polls for completion.
        """
        result = self.client.submit_document(pdf_path)
        self.doc_id = result["doc_id"]
        
        # Polling for completion
        while True:
            doc_info = self.client.get_document(self.doc_id)
            status = doc_info.get("status")
            
            if progress_callback:
                progress_callback(status)
                
            if status == "completed":
                break
            elif status == "failed":
                raise Exception(f"PageIndex processing failed: {doc_info.get('error', 'Unknown error')}")
                
            time.sleep(2) # Poll every 2 seconds
            
        # Fetch tree
        tree_res = self.client.get_tree(self.doc_id)
        self.tree = tree_res.get("result", {})
        return self.tree

    def chat(self, query: str, history=None):
        """
        Uses PageIndex Chat API for reasoning-based retrieval.
        """
        if not self.doc_id:
            raise Exception("No document ingested yet.")

        messages = [{"role": "user", "content": query}]
        if history:
            # Format history if provided (PageIndex expects OpenAI-style messages)
            messages = history + messages

        response = self.client.chat_completions(
            messages=messages,
            doc_id=self.doc_id
        )
        
        # Note: PageIndex Chat API (beta) includes reasoning under the hood.
        # The response structure follows OpenAI's format.
        content = response["choices"][0]["message"]["content"]
        
        # PageIndex often includes citations and structural reasoning in the content
        # or in additional fields if available.
        return {
            "answer": content,
            "reasoning": "Powered by PageIndex Reasoning Agent", # Placeholder or extract if available
            "doc_id": self.doc_id
        }
