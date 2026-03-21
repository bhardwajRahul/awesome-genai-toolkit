from agents import create_host_agent, create_expert_agent, create_summarizer_agent
from memory_db import save_episode
import logging
import time

logger = logging.getLogger(__name__)

MAX_RETRIES = 2
RETRY_DELAY = 10  # seconds between API calls on rate limit


def _run_with_retry(agent, prompt: str) -> str:
    """Run agent with retry on rate limit errors."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = agent.run(prompt)
            return resp.content if isinstance(resp.content, str) else str(resp.content)
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < MAX_RETRIES:
                    logger.warning(f"Rate limited, waiting {RETRY_DELAY}s... (attempt {attempt + 1})")
                    time.sleep(RETRY_DELAY)
                    continue
            raise
    return ""


def generate_episode(topic: str, num_turns: int = 3, on_segment=None) -> dict:
    """Generate a podcast episode with ping-pong conversation."""
    host = create_host_agent()
    expert = create_expert_agent()

    segments: list[dict] = []

    for turn in range(num_turns):
        # --- Host turn ---
        if turn == 0:
            prompt = (
                f"Start a podcast episode about: {topic}. "
                "Quick intro, then ask your first question."
            )
        elif turn == num_turns - 1:
            prompt = (
                f'Expert said: "{segments[-1]["text"]}"\n'
                "Wrap up the episode — final question or closing thought."
            )
        else:
            prompt = (
                f'Expert said: "{segments[-1]["text"]}"\n'
                "React briefly, then ask a follow-up."
            )

        # Small delay between calls to avoid rate limits
        if turn > 0:
            time.sleep(2)

        host_text = _run_with_retry(host, prompt)
        host_segment = {"speaker": "Host (Alex)", "text": host_text, "tone": "curious"}
        segments.append(host_segment)
        if on_segment:
            on_segment(host_segment)

        # --- Expert turn ---
        time.sleep(2)  # Rate limit buffer

        expert_prompt = (
            f'Host said: "{host_text}"\n'
            f"Answer about {topic}."
        )
        if turn == num_turns - 1:
            expert_prompt += " Give a memorable closing takeaway."

        expert_text = _run_with_retry(expert, expert_prompt)
        expert_segment = {"speaker": "Expert (Dr. Sam)", "text": expert_text, "tone": "thoughtful"}
        segments.append(expert_segment)
        if on_segment:
            on_segment(expert_segment)

    # --- Summarize (skip if too few API calls remaining) ---
    time.sleep(2)
    try:
        summarizer = create_summarizer_agent()
        summary_response = summarizer.run(
            f"Summarize this podcast about '{topic}':\n\n"
            + "\n".join(f"{s['speaker']}: {s['text']}" for s in segments)
        )
        summary_data = summary_response.content
        summary = summary_data.summary
        key_takeaways = summary_data.key_takeaways
        topics_covered = summary_data.topics_covered
    except Exception as e:
        logger.error(f"Summarizer error: {e}")
        summary = f"A conversation about {topic}."
        key_takeaways = []
        topics_covered = [topic]

    episode_id = save_episode(
        topic=topic,
        summary=summary,
        key_takeaways=key_takeaways,
        segments=segments,
    )

    return {
        "episode_id": episode_id,
        "topic": topic,
        "segments": segments,
        "summary": summary,
        "key_takeaways": key_takeaways,
        "topics_covered": topics_covered,
    }
