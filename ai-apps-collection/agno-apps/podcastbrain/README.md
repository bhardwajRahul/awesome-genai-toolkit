# 🎙️ PodcastBrain — AI Podcast That Learns What You Like

Two AI agents have a dynamic podcast conversation about **any topic you choose**. The host asks tough questions, the expert debates back — and the system **learns your preferences** over time.

Built with **Agno** (multi-agent framework), **Google Gemini**, **ElevenLabs TTS**, and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red?logo=streamlit&logoColor=white)
![Agno](https://img.shields.io/badge/Agno-2.2+-green)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?logo=google&logoColor=white)
![ElevenLabs](https://img.shields.io/badge/ElevenLabs-TTS-black?logo=elevenlabs)

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT UI                             │
│  ┌──────────┐  ┌──────────────────────────────────────────┐     │
│  │ Sidebar  │  │              Main Area                   │     │
│  │          │  │                                          │     │
│  │ Topic    │  │  🎤 Host (Alex):  "Welcome! Let's talk  │     │
│  │ Input    │  │                    about AI agents..."   │     │
│  │          │  │                                          │     │
│  │ Turns    │  │  🧠 Expert (Sam): "Think of agents like │     │
│  │ Slider   │  │                    interns with a plan"  │     │
│  │          │  │                                          │     │
│  │ Generate │  │  🎤 Host (Alex):  "Wait, so you're     │     │
│  │ Button   │  │                    saying..."            │     │
│  │          │  │                                          │     │
│  │ Past     │  │  🔊 [Audio Player]                      │     │
│  │ Episodes │  │                                          │     │
│  │          │  │  👍 Liked it!  👎 Not great              │     │
│  │ Settings │  │                                          │     │
│  └──────────┘  └──────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## Architecture

```
                    ┌─────────────┐
                    │  User picks │
                    │   a topic   │
                    └──────┬──────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Podcast Orchestrator │
              │      (podcast.py)      │
              └────┬──────────────┬────┘
                   │              │
          ┌────────▼───────┐ ┌───▼────────────┐
          │  🎤 Host Agent │ │ 🧠 Expert Agent │
          │    (Alex)      │ │   (Dr. Sam)     │
          │                │ │                 │
          │ • Asks sharp   │ │ • Deep insights │
          │   questions    │ │ • Debates back  │
          │ • Reacts       │ │ • Uses Reasoning│
          │   naturally    │ │   Tools to think│
          │ • Wraps up     │ │ • Cracks jokes  │
          └────────┬───────┘ └───┬────────────┘
                   │              │
                   ▼              ▼
          ┌────────────────────────────┐
          │    Turn-by-Turn Convo      │
          │                            │
          │  Host  ──► Expert ──►      │
          │  Host  ──► Expert ──►      │
          │  Host  ──► Expert          │
          └─────────────┬──────────────┘
                        │
               ┌────────▼────────┐
               │ 📝 Summarizer   │
               │    Agent        │
               │ (structured     │
               │  output)        │
               └────────┬────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
   ┌────────────┐ ┌──────────┐ ┌───────────┐
   │  SQLite DB │ │ ElevenLabs│ │ Streamlit │
   │            │ │   TTS     │ │    UI     │
   │ • Episodes │ │           │ │           │
   │ • Ratings  │ │ • Host    │ │ • Player  │
   │ • Prefs    │ │   voice   │ │ • Chat    │
   │ • Memory   │ │ • Expert  │ │   bubbles │
   │            │ │   voice   │ │ • Rating  │
   └────────────┘ └──────────┘ └───────────┘
```

## Agno Features Used

```
┌──────────────────────────────────────────────────────────┐
│                    AGNO FRAMEWORK                        │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │   Agent()    │  │ ReasoningTools│  │  SqliteDb()    │  │
│  │             │  │              │  │               │  │
│  │ • Gemini    │  │ • think()    │  │ • Sessions    │  │
│  │   model     │  │ • analyze()  │  │ • Memory      │  │
│  │ • Instructions│ │              │  │ • Persistence │  │
│  │ • output_   │  │ Expert agent │  │               │  │
│  │   schema    │  │ reasons step │  │ Both agents   │  │
│  │             │  │ by step      │  │ learn & adapt │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
│                                                          │
│  ┌─────────────────────┐  ┌───────────────────────────┐  │
│  │  Agentic Memory     │  │  Structured Output        │  │
│  │                     │  │                           │  │
│  │ enable_agentic_     │  │ output_schema=Pydantic    │  │
│  │ memory=True         │  │ model for summarizer      │  │
│  │                     │  │                           │  │
│  │ Agents remember     │  │ Guaranteed JSON schema    │  │
│  │ past conversations  │  │ for episode summaries     │  │
│  └─────────────────────┘  └───────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Learning Loop

```
   Generate Episode
         │
         ▼
   Listen & Read ──────────────┐
         │                     │
         ▼                     ▼
   👍 or 👎 Rating      Set Preferences
         │              (knowledge level,
         │               depth, tone)
         ▼                     │
   Store in SQLite ◄───────────┘
         │
         ▼
   Next Episode ──► Agents read preferences
                    & adapt their style
                          │
                          ▼
                  "Listener enjoys AI topics,
                   prefers deep-dive, advanced
                   level, conversational tone"
```

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/podcastbrain.git
cd podcastbrain
pip install -r requirements.txt
```

### 2. Set API Keys

```bash
cp .env.example .env
```

Edit `.env`:
```
GOOGLE_API_KEY=your-google-api-key
ELEVENLABS_API_KEY=your-elevenlabs-key    # optional — text-only mode works without it
```

Get your keys:
- **Google AI** (required): [aistudio.google.com](https://aistudio.google.com/apikey)
- **ElevenLabs** (optional): [elevenlabs.io](https://elevenlabs.io) — for voice output

### 3. Run

```bash
streamlit run app.py
```

---

## Project Structure

```
podcastbrain/
├── app.py              # Streamlit UI — player, transcript, ratings
├── agents.py           # Host & Expert agent definitions (Agno + Gemini)
├── podcast.py          # Turn-by-turn conversation orchestration
├── audio.py            # ElevenLabs TTS — two distinct voices
├── memory_db.py        # SQLite — episodes, preferences, learning
├── models.py           # Pydantic schemas for structured output
├── requirements.txt    # Dependencies
├── .env.example        # API key template
└── README.md
```

## File Responsibilities

| File | What it does |
|------|-------------|
| `app.py` | Streamlit UI with chat bubbles, audio player, sidebar controls, rating system |
| `agents.py` | Creates 3 Agno agents: Host (Alex), Expert (Dr. Sam), Summarizer |
| `podcast.py` | Ping-pong orchestrator — runs host/expert turns, handles retries & rate limits |
| `audio.py` | ElevenLabs TTS with different voices per speaker, MP3 concatenation |
| `memory_db.py` | SQLite layer for episodes, ratings, user preferences, liked topics |
| `models.py` | Pydantic models: `HostResponse`, `ExpertResponse`, `EpisodeSummary`, `Tone` enum |

---

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Agent Framework | **Agno** | Multi-agent, memory, reasoning tools, structured output |
| LLM | **Google Gemini 2.5 Flash** | Fast, cheap, great for conversation |
| TTS | **ElevenLabs** | Natural voices, two distinct speakers |
| UI | **Streamlit** | Rapid prototyping, audio player built-in |
| Database | **SQLite** | Zero setup, file-based persistence |
| Validation | **Pydantic** | Type-safe structured output schemas |

---

## Features

- **Two-Agent Podcast**: Host asks questions, Expert debates back — real conversation dynamics
- **Learning System**: Rate episodes, set preferences — agents adapt their style over time
- **Agentic Memory**: Agents remember past conversations using Agno's memory system
- **Reasoning Tools**: Expert agent uses `think()` and `analyze()` to reason step-by-step
- **Voice Output**: Two distinct ElevenLabs voices (or text-only mode without API key)
- **Episode History**: Replay past episodes, see ratings and summaries
- **Rate Limit Handling**: Auto-retry with backoff on Gemini API rate limits
- **Structured Summaries**: Summarizer agent outputs guaranteed JSON schema

---

## Configuration

### Listener Profile (in-app)

Set these in the sidebar to personalize episodes:

| Setting | Options | Effect |
|---------|---------|--------|
| Knowledge Level | beginner / intermediate / advanced | Controls technical depth |
| Preferred Depth | surface / balanced / deep-dive | How detailed the discussion gets |
| Preferred Tone | casual / conversational / academic | Language style |

### Model Selection

Edit `MODEL_ID` in `agents.py` to switch models:

```python
MODEL_ID = "gemini-2.5-flash"     # default — fast & smart
MODEL_ID = "gemini-2.0-flash"     # higher free-tier limits (1500 RPD)
MODEL_ID = "gemini-2.5-pro"       # most capable, slower
```

---

## Rate Limits (Free Tier)

| Model | Requests/Day | Requests/Min |
|-------|-------------|-------------|
| gemini-2.5-flash | 20 | 5 |
| gemini-2.0-flash | 1500 | 15 |
| gemini-2.5-pro | 5 | 2 |

Each 3-turn episode uses **~7 API calls**. Use `gemini-2.0-flash` for the free tier.

---

## License

MIT

---

Built with [Agno](https://agno.com) + [Google Gemini](https://ai.google.dev) + [ElevenLabs](https://elevenlabs.io) + [Streamlit](https://streamlit.io)
