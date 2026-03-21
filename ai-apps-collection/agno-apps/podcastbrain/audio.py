import os
import io
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio_cache")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Voice IDs — ElevenLabs preset voices
HOST_VOICE = "JBFqnCBsd6RMkjVDRZzb"      # George - warm male voice
EXPERT_VOICE = "onwK4e9ZLuTAKqWW03F9"     # Daniel - articulate male voice


def is_elevenlabs_available() -> bool:
    return bool(os.getenv("ELEVENLABS_API_KEY"))


def generate_segment_audio(text: str, speaker: str, segment_index: int, episode_id: int) -> str | None:
    """Generate audio for a single segment. Returns file path or None."""
    if not is_elevenlabs_available():
        return None

    try:
        from elevenlabs import ElevenLabs

        client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

        voice_id = HOST_VOICE if "Host" in speaker else EXPERT_VOICE

        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        # Collect audio bytes from generator
        audio_bytes = b"".join(audio_generator)

        file_path = os.path.join(AUDIO_DIR, f"ep{episode_id}_seg{segment_index}.mp3")
        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        return file_path

    except Exception as e:
        logger.error(f"ElevenLabs TTS error for segment {segment_index}: {e}")
        return None


def generate_episode_audio(segments: list[dict], episode_id: int) -> str | None:
    """Generate and combine audio for all segments. Returns combined file path or None."""
    if not is_elevenlabs_available():
        return None

    segment_files = []
    for i, seg in enumerate(segments):
        path = generate_segment_audio(seg["text"], seg["speaker"], i, episode_id)
        if path:
            segment_files.append(path)

    if not segment_files:
        return None

    # Combine MP3 files by simple concatenation (works for same-format MP3s)
    combined_path = os.path.join(AUDIO_DIR, f"ep{episode_id}_full.mp3")
    with open(combined_path, "wb") as outfile:
        for fpath in segment_files:
            with open(fpath, "rb") as infile:
                outfile.write(infile.read())

    # Clean up individual segment files
    for fpath in segment_files:
        try:
            os.remove(fpath)
        except OSError:
            pass

    return combined_path


def get_episode_audio_path(episode_id: int) -> str | None:
    """Check if audio already exists for an episode."""
    path = os.path.join(AUDIO_DIR, f"ep{episode_id}_full.mp3")
    return path if os.path.exists(path) else None
