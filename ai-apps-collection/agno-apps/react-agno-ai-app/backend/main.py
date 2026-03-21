from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import json
import traceback
from agents import agent

app = FastAPI(title="Agno AI App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    agent_name: str = "default"

@app.get("/api/health")
async def health():
    return {"status": "ok", "model": "anthropic/claude-sonnet-4.6"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = agent.run(request.message)
        return {"response": response.content}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "detail": traceback.format_exc()}
        )

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    def generate():
        try:
            response = agent.run(request.message, stream=True)
            for chunk in response:
                if chunk.content:
                    yield f"data: {json.dumps({'content': chunk.content})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/api/agents")
async def list_agents():
    return {"agents": [
        {"name": "Assistant", "description": "General AI assistant powered by Claude Sonnet 4.6", "icon": "🤖"},
    ]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
