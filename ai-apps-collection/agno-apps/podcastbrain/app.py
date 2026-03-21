import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from memory_db import (
    get_all_episodes,
    get_episode,
    rate_episode,
    add_liked_topic,
    get_all_preferences,
    set_preference,
    get_liked_topics,
)
from podcast import generate_episode
from audio import generate_episode_audio, get_episode_audio_path, is_elevenlabs_available

st.set_page_config(page_title="PodcastBrain", page_icon="🎙️", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    .host-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 85%;
    }
    .expert-bubble {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 85%;
        margin-left: auto;
    }
    .speaker-name {
        font-weight: bold;
        font-size: 0.85em;
        opacity: 0.8;
        margin-bottom: 4px;
    }
    .tone-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75em;
        margin-left: 8px;
    }
    .episode-card {
        border: 1px solid #333;
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        transition: all 0.2s;
    }
    .episode-card:hover {
        border-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "current_episode" not in st.session_state:
    st.session_state.current_episode = None
if "generating" not in st.session_state:
    st.session_state.generating = False
if "live_segments" not in st.session_state:
    st.session_state.live_segments = []

# --- Sidebar ---
with st.sidebar:
    st.title("🎙️ PodcastBrain")
    st.caption("AI Podcast That Learns What You Like")

    st.divider()

    # --- Generate New Episode ---
    st.subheader("New Episode")
    topic = st.text_input(
        "Topic",
        placeholder="e.g. The future of AI agents",
        help="Enter any topic for your podcast episode",
    )
    num_turns = st.slider("Conversation Turns", min_value=3, max_value=10, value=5)

    generate_btn = st.button(
        "🎬 Generate Episode",
        use_container_width=True,
        disabled=not topic or st.session_state.generating,
        type="primary",
    )

    tts_status = "🟢 ElevenLabs Connected" if is_elevenlabs_available() else "⚪ Text-only mode (no ElevenLabs key)"
    st.caption(tts_status)

    st.divider()

    # --- Episode History ---
    st.subheader("Past Episodes")
    episodes = get_all_episodes()
    if episodes:
        for ep in episodes:
            rating_str = "⭐" * ep["rating"] if ep["rating"] > 0 else ""
            if st.button(f"📻 {ep['topic'][:30]}... {rating_str}", key=f"ep_{ep['id']}", use_container_width=True):
                st.session_state.current_episode = get_episode(ep["id"])
                st.rerun()
    else:
        st.caption("No episodes yet. Generate your first one!")

    st.divider()

    # --- Listener Preferences ---
    with st.expander("⚙️ Listener Profile"):
        prefs = get_all_preferences()
        knowledge = st.selectbox(
            "Knowledge Level",
            ["beginner", "intermediate", "advanced"],
            index=["beginner", "intermediate", "advanced"].index(prefs.get("knowledge_level", "intermediate")),
        )
        depth = st.selectbox(
            "Preferred Depth",
            ["surface", "balanced", "deep-dive"],
            index=["surface", "balanced", "deep-dive"].index(prefs.get("preferred_depth", "balanced")),
        )
        tone = st.selectbox(
            "Preferred Tone",
            ["casual", "conversational", "academic"],
            index=["casual", "conversational", "academic"].index(prefs.get("preferred_tone", "conversational")),
        )
        if st.button("Save Preferences", use_container_width=True):
            set_preference("knowledge_level", knowledge)
            set_preference("preferred_depth", depth)
            set_preference("preferred_tone", tone)
            st.success("Preferences saved!")

    # --- Liked Topics ---
    liked = get_liked_topics()
    if liked:
        with st.expander("❤️ Liked Topics"):
            for t in liked:
                st.caption(f"• {t}")


# --- Main Area ---

# --- Generate Episode Logic ---
if generate_btn and topic:
    st.session_state.generating = True
    st.session_state.live_segments = []
    st.session_state.current_episode = None

    progress_container = st.container()
    with progress_container:
        st.subheader(f"🎙️ Generating: {topic}")
        status = st.status("Creating your podcast episode...", expanded=True)
        segment_area = st.empty()

        def on_segment(seg):
            st.session_state.live_segments.append(seg)
            # Update the display
            transcript_md = ""
            for s in st.session_state.live_segments:
                icon = "🎤" if "Host" in s["speaker"] else "🧠"
                transcript_md += f"\n\n{icon} **{s['speaker']}** _{s['tone']}_\n\n{s['text']}"
            segment_area.markdown(transcript_md)

        with status:
            st.write("🤖 Agents are conversing...")
            result = generate_episode(topic, num_turns=num_turns, on_segment=on_segment)

            st.write("🔊 Generating audio..." if is_elevenlabs_available() else "✅ Transcript complete!")
            if is_elevenlabs_available():
                audio_path = generate_episode_audio(result["segments"], result["episode_id"])
                result["audio_path"] = audio_path

            status.update(label="Episode complete!", state="complete")

        st.session_state.current_episode = result
        st.session_state.generating = False
        st.rerun()


# --- Display Current Episode ---
if st.session_state.current_episode:
    ep = st.session_state.current_episode

    st.header(f"🎙️ {ep['topic']}")

    # --- Audio Player ---
    audio_path = ep.get("audio_path") or get_episode_audio_path(ep.get("episode_id", 0))
    if audio_path and os.path.exists(audio_path):
        st.audio(audio_path, format="audio/mp3")

    # --- Summary ---
    with st.expander("📋 Episode Summary", expanded=True):
        st.write(ep.get("summary", ""))
        takeaways = ep.get("key_takeaways", [])
        if takeaways:
            st.markdown("**Key Takeaways:**")
            for t in takeaways:
                st.markdown(f"- {t}")

    # --- Transcript ---
    st.subheader("💬 Transcript")
    for seg in ep.get("segments", []):
        if "Host" in seg["speaker"]:
            st.markdown(
                f'<div class="host-bubble">'
                f'<div class="speaker-name">🎤 {seg["speaker"]}<span class="tone-badge">{seg["tone"]}</span></div>'
                f'{seg["text"]}'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="expert-bubble">'
                f'<div class="speaker-name">🧠 {seg["speaker"]}<span class="tone-badge">{seg["tone"]}</span></div>'
                f'{seg["text"]}'
                f'</div>',
                unsafe_allow_html=True,
            )

    # --- Rating ---
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 2])
    episode_id = ep.get("episode_id", ep.get("id"))

    with col1:
        if st.button("👍 Liked it!", use_container_width=True):
            if episode_id:
                rate_episode(episode_id, 5)
                add_liked_topic(ep["topic"])
                st.toast("Thanks! We'll learn from this.")
                st.rerun()

    with col2:
        if st.button("👎 Not great", use_container_width=True):
            if episode_id:
                rate_episode(episode_id, 1)
                st.toast("Got it. We'll adapt!")
                st.rerun()

    with col3:
        rating = ep.get("rating", 0)
        if rating > 0:
            st.caption(f"Your rating: {'⭐' * rating}")

else:
    # --- Welcome Screen ---
    st.title("🎙️ Welcome to PodcastBrain")
    st.markdown("""
    **Your AI podcast that learns what you like.**

    Two AI agents — **Alex** (the host) and **Dr. Sam** (the expert) — will have
    a dynamic, engaging podcast conversation about any topic you choose.

    **How it works:**
    1. Enter a topic in the sidebar
    2. Choose how many conversation turns you want
    3. Hit **Generate Episode**
    4. Listen to the conversation and rate it
    5. PodcastBrain learns your preferences and adapts future episodes

    **Features:**
    - 🧠 Learning system that adapts to your interests and knowledge level
    - 🎭 Natural back-and-forth with debate, humor, and deep insights
    - 🔊 Text-to-speech with distinct voices (when ElevenLabs is configured)
    - 📚 Episode history and replay
    """)

    if not os.getenv("GOOGLE_API_KEY"):
        st.warning("Set your `GOOGLE_API_KEY` in the `.env` file to get started.")
    if not is_elevenlabs_available():
        st.info("Add an `ELEVENLABS_API_KEY` to `.env` for voice output. Text-only mode works without it.")
