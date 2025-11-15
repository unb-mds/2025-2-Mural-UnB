import { useEffect } from "react"
import { allTags as tagsFromData } from "../../data/tags"

interface Tag {
  id: string
  label: string
}

interface TagsFilterModalProps {
  isOpen: boolean
  onClose: () => void
  tags: Tag[]
  selectedTags: string[]
  onTagToggle: (tagId: string) => void
}

export default function TagsFilterModal({ isOpen, onClose, tags, selectedTags, onTagToggle }: TagsFilterModalProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden"
    } else {
      document.body.style.overflow = "unset"
    }
    return () => {
      document.body.style.overflow = "unset"
    }
  }, [isOpen])

  if (!isOpen) return null

  // Agrupar tags por categoria usando a estrutura de allTags
  const tagsByCategory: { [key: string]: Tag[] } = {}
  
  Object.entries(tagsFromData).forEach(([category, categoryTags]) => {
    const matchingTags = categoryTags.filter((categoryTag) =>
      tags.some((tag) => tag.id === categoryTag.id)
    )
    if (matchingTags.length > 0) {
      tagsByCategory[category] = matchingTags
    }
  })

  // Adicionar tags que não estão em nenhuma categoria
  const categorizedTagIds = new Set(Object.values(tagsByCategory).flat().map((t) => t.id))
  const uncategorizedTags = tags.filter((tag) => !categorizedTagIds.has(tag.id))
  
  if (uncategorizedTags.length > 0) {
    tagsByCategory["Outros"] = uncategorizedTags
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Filtrar por Tags</h2>
          <button className="modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-body">
          {Object.entries(tagsByCategory).map(([category, categoryTags]) => (
            <div key={category} className="tag-category">
              <h3>{category}</h3>
              <div className="tags-list">
                {categoryTags.map((tag) => {
                  const isSelected = selectedTags.includes(tag.id)
                  return (
                    <button
                      key={tag.id}
                      onClick={() => onTagToggle(tag.id)}
                      className={`tag-button ${isSelected ? "selected" : ""}`}
                    >
                      {tag.label}
                      {isSelected && <span className="tag-check">✓</span>}
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </div>

        <div className="modal-footer">
          <button onClick={onClose} className="modal-close-button">
            Fechar
          </button>
          <button
            onClick={() => {
              selectedTags.forEach(onTagToggle)
            }}
            className="modal-clear-button"
            disabled={selectedTags.length === 0}
          >
            Limpar Seleção ({selectedTags.length})
          </button>
        </div>
      </div>
    </div>
  )
}

