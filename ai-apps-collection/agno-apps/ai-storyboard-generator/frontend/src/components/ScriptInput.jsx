import { useState } from 'react'
import { PenLine, Settings2, Lightbulb, Wand2, Loader2, Sparkles, Cpu, Palette } from 'lucide-react'

const EXAMPLE_SCRIPTS = [
    "A lone astronaut floats toward a distant nebula. She discovers an alien signal. Her ship powers down. In the darkness, a massive structure emerges from the void.",
    "A detective enters a rain-soaked alley. He spots a cryptic symbol on the wall. A shadowy figure disappears around the corner. He finds a pocket watch — his own, from the future.",
    "A young girl opens a mysterious door in her grandmother's attic. She steps into a sprawling forest of giant glowing mushrooms. A fox with golden eyes guides her deeper in. She finds a small cottage with her name carved above the door.",
]

const TEXT_MODELS = [
    { id: "google/gemini-2.0-flash-001",                            label: "Gemini 2.0 Flash" },
    { id: "meta-llama/llama-3.3-70b-instruct:free",                 label: "Llama 3.3 70B (Free)" },
    { id: "mistralai/mistral-small-3.1-24b-instruct:free",          label: "Mistral Small 3.1 (Free)" },
    { id: "google/gemma-3-27b-it:free",                             label: "Gemma 3 27B (Free)" },
    { id: "nousresearch/hermes-3-llama-3.1-405b:free",              label: "Hermes 3 405B (Free)" },
    { id: "nvidia/nemotron-nano-9b-v2:free",                        label: "Nemotron Nano 9B (Free)" },
]

const ART_STYLES = [
    { id: "pencil",     label: "✏️  Pencil Sketch",  desc: "Classic B&W pencil sketch with ink wash — timeless storyboard look." },
    { id: "watercolor", label: "🎨  Watercolor",       desc: "Soft washes and loose brushwork with a muted cinematic palette." },
    { id: "noir",       label: "🎭  Film Noir",        desc: "Extreme chiaroscuro, deep shadows, 1940s cinematic aesthetic." },
    { id: "comic",      label: "💥  Comic Book",       desc: "Bold outlines, dynamic composition, vibrant colors and action lines." },
    { id: "anime",      label: "⛩️  Anime",            desc: "Cel-shaded style with clean linework and dramatic lighting." },
]

export default function ScriptInput({ onGenerate, loading }) {
    const [script, setScript] = useState('')
    const [numFrames, setNumFrames] = useState(4)
    const [textModel, setTextModel] = useState(TEXT_MODELS[0].id)
    const [style, setStyle] = useState('pencil')

    const handleSubmit = (e) => {
        e.preventDefault()
        if (!script.trim() || loading) return
        onGenerate({ script: script.trim(), numFrames, style, textModel })
    }

    const loadExample = () => {
        const example = EXAMPLE_SCRIPTS[Math.floor(Math.random() * EXAMPLE_SCRIPTS.length)]
        setScript(example)
    }

    const selectedStyleInfo = ART_STYLES.find(s => s.id === style)

    return (
        <div className="script-input">
            <h2>
                <PenLine className="section-icon" size={18} />
                Script Input
            </h2>

            <form onSubmit={handleSubmit} style={{ display: 'contents' }}>
                <div>
                    <label className="input-label">Scene Description / Script</label>
                    <textarea
                        id="script-textarea"
                        className="script-textarea"
                        placeholder="Describe your scene or paste a script excerpt…&#10;&#10;e.g. A detective enters a dark alley. He spots a clue. A car speeds away."
                        value={script}
                        onChange={(e) => setScript(e.target.value)}
                        disabled={loading}
                    />
                </div>

                <div>
                    <label className="input-label" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <Settings2 size={12} />
                        Number of Frames
                    </label>
                    <div className="slider-row">
                        <input
                            id="frames-slider"
                            type="range"
                            min={1}
                            max={8}
                            value={numFrames}
                            onChange={(e) => setNumFrames(Number(e.target.value))}
                            className="frames-slider"
                            disabled={loading}
                        />
                        <span className="frames-badge">{numFrames}</span>
                    </div>
                </div>

                <div>
                    <label className="input-label" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <Palette size={12} />
                        Art Style
                    </label>
                    <select
                        className="tech-select"
                        value={style}
                        onChange={(e) => setStyle(e.target.value)}
                        disabled={loading}
                    >
                        {ART_STYLES.map(s => (
                            <option key={s.id} value={s.id}>{s.label}</option>
                        ))}
                    </select>
                    {selectedStyleInfo && (
                        <p className="style-desc">{selectedStyleInfo.desc}</p>
                    )}
                </div>

                <div>
                    <label className="input-label" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <Cpu size={12} />
                        Director Model
                        <span className="powered-by-or">via OpenRouter</span>
                    </label>
                    <select
                        className="tech-select"
                        value={textModel}
                        onChange={(e) => setTextModel(e.target.value)}
                        disabled={loading}
                    >
                        {TEXT_MODELS.map(m => (
                            <option key={m.id} value={m.id}>{m.label}</option>
                        ))}
                    </select>
                </div>

                <button
                    id="generate-btn"
                    type="submit"
                    className="generate-btn"
                    disabled={loading || !script.trim()}
                >
                    {loading ? (
                        <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10 }}>
                            <Loader2 className="animate-spin" size={18} />
                            Generating…
                        </span>
                    ) : (
                        <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10 }}>
                            <Wand2 size={18} />
                            Generate Storyboard
                        </span>
                    )}
                </button>
            </form>

            <button
                id="example-btn"
                onClick={loadExample}
                disabled={loading}
                className="action-bar-btn"
                style={{
                    background: 'none',
                    border: '1px dashed var(--border-bright)',
                    color: 'var(--text-secondary)',
                    padding: '12px',
                    borderRadius: 'var(--radius-md)',
                    cursor: 'pointer',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                    width: '100%',
                    transition: 'all 0.2s',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: 8
                }}
                onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--gold)'; e.currentTarget.style.color = 'var(--gold)'; e.currentTarget.style.background = 'var(--gold-muted)' }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border-bright)'; e.currentTarget.style.color = 'var(--text-secondary)'; e.currentTarget.style.background = 'none' }}
            >
                <Sparkles size={14} />
                Load Example Script
            </button>

            <div className="tips-box">
                <h3>
                    <Lightbulb size={12} style={{ marginRight: 8, verticalAlign: 'middle' }} />
                    Pro Tips
                </h3>
                <ul>
                    <li><span>✦</span> Use vivid, action-oriented language.</li>
                    <li><span>✦</span> Mention lighting (e.g., "Golden Hour").</li>
                    <li><span>✦</span> Suggest camera angles (e.g., "Low Angle").</li>
                </ul>
            </div>
        </div>
    )
}
