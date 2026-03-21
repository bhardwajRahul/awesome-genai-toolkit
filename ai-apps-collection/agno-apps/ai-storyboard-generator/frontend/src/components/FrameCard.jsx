import { useState } from 'react'
import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { GripVertical, Trash2, Download, ImageOff, RefreshCw } from 'lucide-react'

export default function FrameCard({ frame, onDelete, onRegenerate }) {
    const [regenerating, setRegenerating] = useState(false)

    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ id: frame.id })

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
    }

    const imgSrc = frame.image_base64
        ? `data:${frame.mime_type || 'image/png'};base64,${frame.image_base64}`
        : null

    const handleDownload = (e) => {
        e.stopPropagation()
        if (!imgSrc) return
        const link = document.createElement('a')
        link.download = `frame-${frame.frame_number}-${Date.now()}.png`
        link.href = imgSrc
        link.click()
    }

    const handleRegenerate = async (e) => {
        e.stopPropagation()
        if (regenerating) return
        setRegenerating(true)
        try {
            await onRegenerate(frame)
        } finally {
            setRegenerating(false)
        }
    }

    return (
        <div
            ref={setNodeRef}
            style={style}
            className={`frame-card ${isDragging ? 'dragging' : ''}`}
            id={`frame-card-${frame.id}`}
        >
            {/* Image or placeholder */}
            {imgSrc ? (
                <div className="frame-image-wrap">
                    <img src={imgSrc} alt={`Frame ${frame.frame_number}`} loading="lazy" />
                    <div className="frame-overlay">
                        <p>{frame.scene_description}</p>
                    </div>
                </div>
            ) : (
                <div className="frame-no-image">
                    <ImageOff size={24} opacity={0.3} />
                    <p>No Image</p>
                </div>
            )}

            {/* Controls */}
            <div className="frame-controls">
                <button
                    className="ctrl-btn btn-drag"
                    title="Drag to reorder"
                    {...attributes}
                    {...listeners}
                >
                    <GripVertical size={14} />
                </button>
                <button
                    className={`ctrl-btn btn-regen ${regenerating ? 'spinning' : ''}`}
                    title="Regenerate frame"
                    onClick={handleRegenerate}
                    disabled={regenerating}
                >
                    <RefreshCw size={14} />
                </button>
                {imgSrc && (
                    <button
                        className="ctrl-btn btn-download"
                        title="Download Frame"
                        onClick={handleDownload}
                    >
                        <Download size={14} />
                    </button>
                )}
                <button
                    className="ctrl-btn btn-delete"
                    title="Remove frame"
                    onClick={(e) => { e.stopPropagation(); onDelete(frame.id); }}
                    id={`delete-frame-${frame.id}`}
                >
                    <Trash2 size={14} />
                </button>
            </div>

            {/* Caption */}
            <div className="frame-meta">
                <span className="frame-number-badge">#{frame.frame_number}</span>
                <p className="frame-caption">
                    {frame.caption || frame.scene_description}
                </p>
            </div>
        </div>
    )
}
