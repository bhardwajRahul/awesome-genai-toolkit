import { useState } from 'react'
import { Clapperboard, Sparkles } from 'lucide-react'
import './App.css'
import ScriptInput from './components/ScriptInput'
import StoryboardTimeline from './components/StoryboardTimeline'

const API_BASE = 'http://localhost:8000'
const IMAGE_MODEL = 'google/gemini-3.1-flash-image-preview'

export default function App() {
  const [frames, setFrames] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState(0)
  const [progressLabel, setProgressLabel] = useState('')
  const [currentStyle, setCurrentStyle] = useState('pencil')

  const handleGenerate = async ({ script, numFrames, style, textModel }) => {
    setLoading(true)
    setError(null)
    setFrames([])
    setProgress(5)
    setProgressLabel('Director Agent analyzing script…')
    setCurrentStyle(style)

    let framesReceived = 0
    let totalExpected = numFrames
    let lastEventType = ''

    try {
      const res = await fetch(`${API_BASE}/generate-storyboard-stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          script,
          num_frames: numFrames,
          style,
          text_model: textModel,
          image_model: IMAGE_MODEL,
        }),
      })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || `Server error: ${res.status}`)
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() // keep incomplete last line

        for (const line of lines) {
          const trimmed = line.trim()
          if (trimmed.startsWith('event: ')) {
            lastEventType = trimmed.slice(7)
          } else if (trimmed.startsWith('data: ')) {
            let data
            try {
              data = JSON.parse(trimmed.slice(6))
            } catch {
              continue
            }

            if (lastEventType === 'status') {
              if (data.stage === 'splitting') {
                setProgressLabel('Director Agent splitting script into scenes…')
                setProgress(15)
              } else if (data.stage === 'generating') {
                totalExpected = data.total
                setProgressLabel(`Generating ${data.total} frames in parallel…`)
                setProgress(30)
              }
            } else if (lastEventType === 'frame') {
              framesReceived++
              setFrames(prev => [...prev, data])
              const pct = 30 + (framesReceived / totalExpected) * 68
              setProgress(Math.min(pct, 98))
              setProgressLabel(`Frame ${framesReceived} of ${totalExpected} ready…`)
            } else if (lastEventType === 'done') {
              setProgress(100)
              setProgressLabel('Complete!')
            } else if (lastEventType === 'error') {
              throw new Error(data.detail || 'Generation failed')
            }
          }
        }
      }

      setTimeout(() => {
        setLoading(false)
        setProgress(0)
      }, 500)
    } catch (err) {
      setError(err.message)
      setLoading(false)
      setProgress(0)
    }
  }

  const handleReorder = (newFrames) => {
    setFrames(newFrames)
  }

  const handleDelete = (id) => {
    setFrames(prev => prev.filter(f => f.id !== id))
  }

  const handleRegenerate = async (frame) => {
    try {
      const res = await fetch(`${API_BASE}/regenerate-frame`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scene_description: frame.scene_description,
          frame_number: frame.frame_number,
          total_frames: frames.length,
          style: currentStyle,
          image_model: IMAGE_MODEL,
        }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || `Server error: ${res.status}`)
      }
      const newFrame = await res.json()
      // Replace the frame in state, keeping the same id for React key stability
      setFrames(prev => prev.map(f => f.id === frame.id ? { ...newFrame, id: frame.id } : f))
    } catch (err) {
      console.error('Regenerate failed:', err)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo-icon">
          <Clapperboard color="var(--gold)" size={24} />
        </div>
        <h1>Storyboarder <span style={{ color: 'var(--gold)', fontSize: '0.8em', verticalAlign: 'middle' }}>AI</span></h1>

        <div className="header-badges">
          <a
            href="https://agno.com"
            target="_blank"
            rel="noreferrer"
            className="tech-badge agno-badge"
          >
            <span className="badge-dot" />
            Agno
          </a>
          <span className="badge-sep">×</span>
          <a
            href="https://openrouter.ai"
            target="_blank"
            rel="noreferrer"
            className="tech-badge openrouter-badge"
          >
            <span className="badge-dot" />
            OpenRouter
          </a>
          <span className="badge-sep">×</span>
          <span className="tech-badge model-badge">Gemini 3.1 Flash</span>
        </div>

        <div className="tagline">
          <Sparkles size={12} style={{ marginRight: 6 }} />
          Multi-Agent Cinema AI
        </div>
      </header>

      <div className="app-body">
        <aside className="left-panel">
          <ScriptInput onGenerate={handleGenerate} loading={loading} />
        </aside>

        <main className="right-panel">
          <StoryboardTimeline
            frames={frames}
            loading={loading}
            error={error}
            progress={progress}
            progressLabel={progressLabel}
            onReorder={handleReorder}
            onDelete={handleDelete}
            onRegenerate={handleRegenerate}
          />
        </main>
      </div>
    </div>
  )
}
