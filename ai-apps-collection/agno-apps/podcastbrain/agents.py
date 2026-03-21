import os
from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.db.sqlite import SqliteDb

from models import EpisodeSummary
from memory_db import get_all_preferences, get_liked_topics, get_past_topics

MEMORY_DB_PATH = os.path.join(os.path.dirname(__file__), "podcastbrain.db")

# Use gemini-2.0-flash for higher free-tier rate limits (1500 RPD vs 20 RPD)
MODEL_ID = "gemini-2.5-flash"


def _build_preference_context() -> str:
    prefs = get_all_preferences()
    liked = get_liked_topics()
    past = get_past_topics()

    lines = []
    if liked:
        lines.append(f"Topics the listener has enjoyed before: {', '.join(liked)}")
    if past:
        lines.append(f"Recent episode topics: {', '.join(past[:5])}")
    if prefs.get("knowledge_level"):
        lines.append(f"Listener's knowledge level: {prefs['knowledge_level']}")
    if prefs.get("preferred_depth"):
        lines.append(f"Preferred depth: {prefs['preferred_depth']}")
    if prefs.get("preferred_tone"):
        lines.append(f"Preferred tone: {prefs['preferred_tone']}")

    return "\n".join(lines) if lines else "No listener preferences yet."


def create_host_agent() -> Agent:
    pref_context = _build_preference_context()

    return Agent(
        name="Host",
        model=Gemini(id=MODEL_ID),
        description="You are Alex, a charismatic podcast host.",
        instructions=[
            "You host a fast-paced podcast with an expert guest.",
            "Ask sharp questions, react naturally, keep it moving.",
            "BE BRIEF: 1-3 short sentences ONLY. No paragraphs. Think Twitter, not essay.",
            "Use natural podcast language: 'Fascinating...', 'Wait, so...', 'Let me push back...'",
            "Respond ONLY with your spoken words. No labels, no formatting, no stage directions.",
            f"\n--- Listener ---\n{pref_context}",
        ],
        db=SqliteDb(db_file=MEMORY_DB_PATH),
        enable_agentic_memory=True,
        markdown=False,
    )


def create_expert_agent() -> Agent:
    pref_context = _build_preference_context()

    return Agent(
        name="Expert",
        model=Gemini(id=MODEL_ID),
        description="You are Dr. Sam, a sharp domain expert.",
        instructions=[
            "You're a guest expert on a podcast.",
            "Give punchy, insightful answers with one vivid example or analogy.",
            "BE BRIEF: 2-4 short sentences ONLY. No paragraphs. No bullet points. No lists.",
            "Debate, joke, surprise the host. Don't lecture.",
            "Respond ONLY with your spoken words. No labels, no formatting, no stage directions.",
            f"\n--- Listener ---\n{pref_context}",
        ],
        tools=[ReasoningTools(enable_think=True, enable_analyze=True)],
        db=SqliteDb(db_file=MEMORY_DB_PATH),
        enable_agentic_memory=True,
        markdown=False,
    )


def create_summarizer_agent() -> Agent:
    return Agent(
        name="Summarizer",
        model=Gemini(id=MODEL_ID),
        description="You summarize podcast episodes briefly.",
        instructions=[
            "Summarize the podcast transcript in 1-2 sentences.",
            "List 2-3 key takeaways and topics covered.",
        ],
        output_schema=EpisodeSummary,
        structured_outputs=True,
        markdown=False,
    )
