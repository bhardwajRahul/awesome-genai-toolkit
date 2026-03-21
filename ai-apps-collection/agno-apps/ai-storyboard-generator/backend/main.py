"""
FastAPI backend for the AI Storyboard Generator.
"""

import json
import os
import uuid
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from agent import _generate_single_frame, generate_storyboard_async, generate_storyboard_stream

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

app = FastAPI(title="AI Storyboard Generator API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class StoryboardRequest(BaseModel):
    script: str = Field(..., min_length=10, description="Script or scene description")
    num_frames: int = Field(default=4, ge=1, le=8, description="Number of storyboard frames")
    style: str = Field(default="pencil", description="Art style: pencil, watercolor, noir, comic, anime")
    text_model: str = Field(default="google/gemini-2.0-flash-001", description="OpenRouter model for scene splitting")
    image_model: str = Field(default="google/gemini-3.1-flash-image-preview", description="OpenRouter model for image generation")


class RegenerateRequest(BaseModel):
    scene_description: str
    frame_number: int
    total_frames: int
    style: str = "pencil"
    image_model: str = "google/gemini-3.1-flash-image-preview"


class FrameResponse(BaseModel):
    id: str
    frame_number: int
    scene_description: str
    caption: str
    image_base64: Optional[str]
    mime_type: str


class StoryboardResponse(BaseModel):
    frames: list[FrameResponse]
    total_frames: int


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}


@app.post("/generate-storyboard", response_model=StoryboardResponse)
async def create_storyboard(req: StoryboardRequest):
    """Non-streaming endpoint — collects all frames then returns (backwards compatible)."""
    try:
        raw_frames = await generate_storyboard_async(
            req.script, req.num_frames, req.style, req.text_model, req.image_model
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    frames = [
        FrameResponse(
            id=str(uuid.uuid4()),
            frame_number=f["frame_number"],
            scene_description=f["scene_description"],
            caption=f["caption"],
            image_base64=f.get("image_base64"),
            mime_type=f.get("mime_type", "image/png"),
        )
        for f in raw_frames
    ]
    return StoryboardResponse(frames=frames, total_frames=len(frames))


@app.post("/generate-storyboard-stream")
async def create_storyboard_stream(req: StoryboardRequest):
    """
    SSE streaming endpoint. Emits one JSON event per frame as it completes.
    Events: status (splitting/generating), frame, done, error
    """
    async def event_generator():
        try:
            async for event in generate_storyboard_stream(
                req.script, req.num_frames, req.style, req.text_model, req.image_model
            ):
                event_type = event.pop("type")
                if event_type == "frame":
                    event["id"] = str(uuid.uuid4())
                yield f"event: {event_type}\ndata: {json.dumps(event)}\n\n"
        except Exception as exc:
            yield f"event: error\ndata: {json.dumps({'detail': str(exc)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.post("/regenerate-frame", response_model=FrameResponse)
async def regenerate_frame(req: RegenerateRequest):
    """Regenerate a single storyboard frame with a new image."""
    try:
        client = AsyncOpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )
        frame = await _generate_single_frame(
            client,
            req.scene_description,
            req.frame_number,
            req.total_frames,
            req.style,
            req.image_model,
        )
        return FrameResponse(
            id=str(uuid.uuid4()),
            frame_number=frame["frame_number"],
            scene_description=frame["scene_description"],
            caption=frame["caption"],
            image_base64=frame.get("image_base64"),
            mime_type=frame.get("mime_type", "image/png"),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
