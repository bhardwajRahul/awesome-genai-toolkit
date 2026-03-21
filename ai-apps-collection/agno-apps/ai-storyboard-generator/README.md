# 🎬 AI Storyboard Generator

> Turn any script or scene description into a sequential cinematic storyboard — powered by **Gemini 3.1 Flash Image Preview** via **OpenRouter**, with a draggable React timeline.

---

## Features

- 📝 **Script-to-storyboard** — paste any script or scene description, choose 1–8 frames
- 🖼️ **Gemini image gen** — each scene rendered as a pencil-sketch cinematic storyboard frame
- 🎞️ **Filmstrip timeline** — horizontal drag-and-drop reordering with `@dnd-kit`
- 🗑️ **Delete frames** — remove unwanted frames from the board
- 📥 **Export** — download the storyboard metadata as JSON
- 🌑 **Dark cinematic theme** — IMDb-style gold + charcoal design

---

## Project Structure

```
ai-storyboard-generator/
├── backend/
│   ├── agent.py         # Scene splitting + Gemini image gen via OpenRouter
│   ├── main.py          # FastAPI app (POST /generate-storyboard)
│   ├── requirements.txt
│   └── .env.example
└── frontend/            # Vite + React
    └── src/
        ├── App.jsx
        ├── App.css
        └── components/
            ├── ScriptInput.jsx
            ├── StoryboardTimeline.jsx
            └── FrameCard.jsx
```

---

## Setup

### 1. Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Add your OpenRouter API key
cp .env.example .env
# Edit .env → OPENROUTER_API_KEY=your_key

# Start the server
uvicorn main:app --reload --port 8000
```

> API docs available at http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

> Open http://localhost:5173

---

## Usage

1. Enter a script or scene description in the left panel
2. Choose how many frames to generate (1–8)
3. Click **🎬 Generate Storyboard**
4. Watch frames appear in the filmstrip timeline
5. **Drag** frames to reorder • **Hover** to see full scene detail • **✕** to delete

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | Your OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai)) |

---

## Models Used

| Task | Model |
|---|---|
| Image generation | `google/gemini-3.1-flash-image-preview` |
| Scene splitting | `google/gemini-3.0-flash` |
