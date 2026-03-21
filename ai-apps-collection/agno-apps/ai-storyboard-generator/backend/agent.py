"""
Storyboard generation agent using Agno + OpenRouter.

Architecture:
  1. DirectorAgent (Agno): Splits the user script into N scene descriptions.
  2. Parallel ImageWorkers (AsyncOpenAI + OpenRouter): Generate one image per scene simultaneously.
     Frames are yielded via an async generator as each one completes (asyncio.wait FIRST_COMPLETED).
"""

import asyncio
import base64
import json
import os
import re
from typing import AsyncGenerator

from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from openai import AsyncOpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
IMAGE_MODEL = "google/gemini-3.1-flash-image-preview"
DEFAULT_TEXT_MODEL = "google/gemini-2.0-flash-001"

# ---------------------------------------------------------------------------
# Art style prompt modifiers
# ---------------------------------------------------------------------------

ART_STYLES = {
    "pencil":     "professional film storyboard, pencil sketch with light ink wash, black-and-white, high contrast, subtle grey tones",
    "watercolor": "professional film storyboard, watercolor painting style, soft washes, loose brushwork, muted cinematic palette",
    "noir":       "professional film storyboard, film noir style, extreme chiaroscuro, deep shadows, high contrast, 1940s cinematic aesthetic",
    "comic":      "professional film storyboard, comic book style, bold outlines, dynamic composition, vibrant colors, action lines",
    "anime":      "professional film storyboard, anime cel-shaded style, clean linework, dramatic lighting, expressive characters",
}

# ---------------------------------------------------------------------------
# Agno DirectorAgent — splits script into scenes
# ---------------------------------------------------------------------------

async def _split_scenes_async(script: str, num_frames: int, text_model: str) -> list[str]:
    """Use Agno DirectorAgent to split the script into N scene descriptions."""
    director = Agent(
        name="DirectorAgent",
        model=OpenRouter(id=text_model),
        instructions=[
            "You are a professional screenplay analyst and storyboard director.",
            f"Split the given script into exactly {num_frames} distinct, vivid, self-contained "
            "scene descriptions suitable for a storyboard artist.",
            "Respond ONLY with a valid JSON array of strings. No markdown fences, no commentary.",
            'Example for 2 frames: ["An astronaut drifts toward a glowing nebula.", '
            '"The nebula pulses — an alien signal. Her ship powers down."]',
        ],
        markdown=False,
    )

    result = await director.arun(
        f"Split this script into exactly {num_frames} scenes:\n\n{script}"
    )

    # Extract text content from RunResponse
    raw = ""
    if hasattr(result, "content") and result.content:
        raw = str(result.content)
    elif hasattr(result, "messages") and result.messages:
        for msg in reversed(result.messages):
            if hasattr(msg, "content") and msg.content:
                raw = str(msg.content)
                break
    else:
        raw = str(result)

    return _parse_scenes(raw, num_frames, script)


def _parse_scenes(raw: str, num_frames: int, fallback: str) -> list[str]:
    """Robustly parse scene descriptions from the director agent's response."""
    scenes: list[str] = []

    # Strip markdown fences if present
    cleaned = re.sub(r"```(?:json)?\n?", "", raw).strip().rstrip("`").strip()

    # Find JSON array in the response
    match = re.search(r'\[.*\]', cleaned, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, list):
                scenes = [str(s).strip() for s in parsed if s]
        except json.JSONDecodeError:
            pass

    # Fallback: line-by-line parsing
    if not scenes:
        for line in raw.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            # Strip leading numbering like "1. " or "1) "
            for sep in [". ", ") ", ": "]:
                if line and line[0].isdigit() and sep in line:
                    _, _, line = line.partition(sep)
                    break
            if line:
                scenes.append(line.strip())

    if not scenes:
        scenes = [fallback]

    # Trim or pad to exactly num_frames
    scenes = scenes[:num_frames]
    while len(scenes) < num_frames:
        scenes.append(scenes[-1] if scenes else fallback)

    return scenes


# ---------------------------------------------------------------------------
# Async image generation for one frame
# ---------------------------------------------------------------------------

def _storyboard_prompt(scene: str, frame_num: int, total_frames: int, style: str) -> str:
    style_desc = ART_STYLES.get(style, ART_STYLES["pencil"])
    return (
        f"Create a cinematic storyboard frame {frame_num} of {total_frames}. "
        f"Scene: {scene}. "
        f"Style: {style_desc}, "
        "dramatic composition, clear focal point, aspect ratio 16:9."
    )


async def _generate_single_frame(
    client: AsyncOpenAI,
    scene: str,
    frame_num: int,
    total_frames: int,
    style: str,
    image_model: str,
) -> dict:
    """Generate one storyboard frame image via OpenRouter (async)."""
    prompt = _storyboard_prompt(scene, frame_num, total_frames, style)

    response = await client.chat.completions.create(
        model=image_model,
        messages=[{"role": "user", "content": prompt}],
        extra_body={"response_modalities": ["TEXT", "IMAGE"]},
    )

    image_b64: str | None = None
    caption: str = scene
    mime_type: str = "image/png"

    choice = response.choices[0]
    content = choice.message.content
    msg = choice.message

    # 1. Try choice.message.images (OpenRouter specific)
    if hasattr(msg, "images") and msg.images:
        for img in msg.images:
            img_dict = img if isinstance(img, dict) else (
                img.model_dump() if hasattr(img, "model_dump") else getattr(img, "__dict__", {})
            )
            if img_dict.get("type") == "image_url":
                url = img_dict.get("image_url", {}).get("url", "")
                if url.startswith("data:"):
                    header, _, data = url.partition(",")
                    mime_type = header.split(":")[1].split(";")[0]
                    image_b64 = data
                else:
                    image_b64 = url
                if image_b64:
                    break

    # 2. Try content list
    if image_b64 is None and isinstance(content, list):
        for part in content:
            if isinstance(part, dict):
                if part.get("type") == "image_url":
                    url: str = part.get("image_url", {}).get("url", "")
                    if url.startswith("data:"):
                        header, _, data = url.partition(",")
                        mime_type = header.split(":")[1].split(";")[0]
                        image_b64 = data
                    else:
                        image_b64 = url
                elif part.get("type") == "text":
                    caption = part.get("text", scene) or scene

    # 3. Try content string data-URL
    elif image_b64 is None and isinstance(content, str):
        if content.startswith("data:"):
            header, _, data = content.partition(",")
            mime_type = header.split(":")[1].split(";")[0]
            image_b64 = data
        else:
            try:
                base64.b64decode(content[:64])
                image_b64 = content
            except Exception:
                caption = content

    # 4. Fallback search in raw response
    if image_b64 is None:
        raw_dict = getattr(response, "__dict__", {})
        images = raw_dict.get("images") or []
        if images:
            img_bytes = images[0].get("content") or images[0].get("data")
            if img_bytes:
                image_b64 = base64.b64encode(img_bytes).decode()

    return {
        "frame_number": frame_num,
        "scene_description": scene,
        "caption": caption[:120] if caption else scene[:120],
        "image_base64": image_b64,
        "mime_type": mime_type,
    }


# ---------------------------------------------------------------------------
# Streaming orchestrator — yields frames as they complete (async generator)
# ---------------------------------------------------------------------------

async def generate_storyboard_stream(
    script: str,
    num_frames: int,
    style: str = "pencil",
    text_model: str = DEFAULT_TEXT_MODEL,
    image_model: str = IMAGE_MODEL,
) -> AsyncGenerator[dict, None]:
    """
    Async generator that yields event dicts:
      {"type": "status", "stage": "splitting"}
      {"type": "status", "stage": "generating", "total": N}
      {"type": "frame", "frame_number": N, ...image data...}
      {"type": "done"}
    """
    yield {"type": "status", "stage": "splitting"}

    scenes = await _split_scenes_async(script, num_frames, text_model)

    yield {"type": "status", "stage": "generating", "total": len(scenes)}

    client = AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
    )

    # Launch all image generation tasks simultaneously
    pending = {
        asyncio.ensure_future(
            _generate_single_frame(client, scene, i + 1, len(scenes), style, image_model)
        )
        for i, scene in enumerate(scenes)
    }

    # Yield each frame as soon as it completes (first-come-first-served)
    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            frame = task.result()
            yield {"type": "frame", **frame}

    yield {"type": "done"}


# ---------------------------------------------------------------------------
# Non-streaming orchestrator — returns all frames (backwards compat)
# ---------------------------------------------------------------------------

async def generate_storyboard_async(
    script: str,
    num_frames: int,
    style: str = "pencil",
    text_model: str = DEFAULT_TEXT_MODEL,
    image_model: str = IMAGE_MODEL,
) -> list[dict]:
    """Collect all frames from the streaming generator and return as a list."""
    frames = []
    async for event in generate_storyboard_stream(script, num_frames, style, text_model, image_model):
        if event["type"] == "frame":
            frames.append({k: v for k, v in event.items() if k != "type"})
    return frames
