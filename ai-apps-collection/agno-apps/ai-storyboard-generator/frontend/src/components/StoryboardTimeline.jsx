import { useRef, useState } from 'react'
import {
    DndContext,
    closestCenter,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors
} from '@dnd-kit/core'
import {
    arrayMove,
    SortableContext,
    sortableKeyboardCoordinates,
    horizontalListSortingStrategy
} from '@dnd-kit/sortable'
import {
    Film,
    Download,
    Share2,
    MousePointer2,
    AlertCircle
} from 'lucide-react'
import html2canvas from 'html2canvas'
import FrameCard from './FrameCard'

export default function StoryboardTimeline({
    frames,
    loading,
    error,
    progress,
    progressLabel,
    onReorder,
    onDelete,
    onRegenerate,
}) {
    const timelineRef = useRef(null)
    const [toast, setToast] = useState(null)

    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: { distance: 6 },
        }),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    )

    const showToast = (msg) => {
        setToast(msg)
        setTimeout(() => setToast(null), 3500)
    }

    const handleDragEnd = (event) => {
        const { active, over } = event
        if (active && over && active.id !== over.id) {
            const oldIndex = frames.findIndex((f) => f.id === active.id)
            const newIndex = frames.findIndex((f) => f.id === over.id)
            onReorder(arrayMove(frames, oldIndex, newIndex))
        }
    }

    const handleExport = async () => {
        if (!timelineRef.current || frames.length === 0) return
        try {
            const canvas = await html2canvas(timelineRef.current, {
                backgroundColor: '#060709',
                useCORS: true,
                scale: 2,
            })
            const link = document.createElement('a')
            link.download = `storyboard-${Date.now()}.png`
            link.href = canvas.toDataURL('image/png')
            link.click()
            showToast('Storyboard exported as PNG!')
        } catch (err) {
            console.error('Export failed', err)
        }
    }

    const handleShare = async () => {
        // Capture storyboard as image
        if (timelineRef.current && frames.length > 0) {
            try {
                const canvas = await html2canvas(timelineRef.current, {
                    backgroundColor: '#060709',
                    useCORS: true,
                    scale: 1.5,
                })
                const link = document.createElement('a')
                link.download = `storyboard-share-${Date.now()}.png`
                link.href = canvas.toDataURL('image/png')
                link.click()
            } catch (err) {
                console.error('Canvas capture failed', err)
            }
        }

        // Open Twitter/X intent
        const tweetText = encodeURIComponent(
            `Generated this ${frames.length}-frame storyboard from a script in seconds! 🎬\n\n` +
            `Built with @agno_api multi-agent pipeline + @OpenRouterAI (Gemini 3.1 Flash)\n\n` +
            `#GenerativeAI #StoryboardAI #OpenRouter #Agno`
        )
        window.open(
            `https://twitter.com/intent/tweet?text=${tweetText}`,
            '_blank',
            'width=550,height=420'
        )

        showToast('Image downloaded — attach it to your tweet!')
    }

    const renderContent = () => {
        if (loading && frames.length === 0) {
            return (
                <div className="skeleton-row">
                    {[1, 2, 3, 4].map((i) => (
                        <div key={i} className="skeleton-card" style={{ animationDelay: `${i * 0.1}s` }}>
                            <div className="skeleton-img" />
                            <div className="skeleton-text">
                                <div className="skeleton-line" />
                                <div className="skeleton-line short" />
                            </div>
                        </div>
                    ))}
                </div>
            )
        }

        if (error) {
            return (
                <div className="error-notice">
                    <AlertCircle size={18} />
                    <span>Error: {error}</span>
                </div>
            )
        }

        if (frames.length === 0) {
            return (
                <div className="empty-state">
                    <div className="empty-icon"><Film size={64} /></div>
                    <h3>Your Storyboard Awaits</h3>
                    <p>Enter a script on the left, pick a style, and watch your frames appear one by one as each agent completes.</p>
                </div>
            )
        }

        return (
            <>
                <div className="filmstrip-track">
                    <div className="filmstrip-wrapper" ref={timelineRef}>
                        <div className="perforations">
                            {Array.from({ length: 24 }).map((_, i) => (
                                <div key={i} className="perf-hole" />
                            ))}
                        </div>
                        <div className="frames-row">
                            <DndContext
                                sensors={sensors}
                                collisionDetection={closestCenter}
                                onDragEnd={handleDragEnd}
                            >
                                <SortableContext
                                    items={frames.map(f => f.id)}
                                    strategy={horizontalListSortingStrategy}
                                >
                                    {frames.map((frame) => (
                                        <FrameCard
                                            key={frame.id}
                                            frame={frame}
                                            onDelete={() => onDelete(frame.id)}
                                            onRegenerate={onRegenerate}
                                        />
                                    ))}
                                </SortableContext>
                            </DndContext>
                        </div>
                        <div className="perforations">
                            {Array.from({ length: 24 }).map((_, i) => (
                                <div key={i} className="perf-hole" />
                            ))}
                        </div>
                        <div className="filmstrip-watermark">
                            <span>Powered by Agno + OpenRouter</span>
                            <span className="watermark-sep">·</span>
                            <span>Gemini 3.1 Flash</span>
                        </div>
                    </div>
                </div>

                <div className="action-bar">
                    <button className="primary" onClick={handleExport}>
                        <Download size={16} />
                        Export PNG
                    </button>
                    <button className="share-btn" onClick={handleShare}>
                        <Share2 size={16} />
                        Share on X
                    </button>
                    <div className="hint">
                        <MousePointer2 size={12} style={{ display: 'inline', verticalAlign: 'middle', marginRight: 6 }} />
                        Drag frames to reorder
                    </div>
                </div>
            </>
        )
    }

    return (
        <div className="timeline-container">
            <div className="timeline-header">
                <h2>
                    <Film size={18} className="section-icon" />
                    Timeline
                </h2>
                <div className="timeline-meta">
                    {frames.length > 0 && (
                        <span className="frame-count-badge">{frames.length} FRAMES</span>
                    )}
                </div>
            </div>

            {(loading || frames.length > 0) && progress > 0 && (
                <div className="generation-progress">
                    <div className="progress-label">{progressLabel}</div>
                    <div className="progress-bar-track">
                        <div
                            className="progress-bar-fill"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                </div>
            )}

            {renderContent()}

            {toast && (
                <div className="toast">
                    {toast}
                </div>
            )}
        </div>
    )
}
