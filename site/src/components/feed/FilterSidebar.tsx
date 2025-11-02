
"use client"

import { useState } from "react"
import TagsFilterModal from "components/feed/TagsFilterModal"
import "./FilterSidebar.css"

interface Tag {
  id: string
  label: string
}

interface FilterSidebarProps {
  tags: Tag[]
  selectedTags: string[]
  onTagToggle: (tagId: string) => void
  searchTerm: string
  onSearchChange: (term: string) => void
}

export default function FilterSidebar({
  tags,
  selectedTags,
  onTagToggle,
  searchTerm,
  onSearchChange,
}: FilterSidebarProps) {
  const [isModalOpen, setIsModalOpen] = useState(false)

  return (
    <>
      <aside className="filter-sidebar">
        <div className="search-box">
          <input
            type="text"
            placeholder="Buscar oportunidades..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="search-input"
          />
        </div>

        <button onClick={() => setIsModalOpen(true)} className="filter-button">
          Filtrar por Tags ({selectedTags.length})
        </button>

        {selectedTags.length > 0 && (
          <div className="selected-tags">
            <h3>Tags Selecionadas:</h3>
            <div className="tags-list">
              {selectedTags.map((tagId) => {
                const tag = tags.find((t) => t.id === tagId)
                return tag ? (
                  <span key={tagId} className="tag selected">
                    {tag.label}
                    <button onClick={() => onTagToggle(tagId)} className="tag-remove">
                      ×
                    </button>
                  </span>
                ) : null
              })}
            </div>
            <button onClick={() => selectedTags.forEach(onTagToggle)} className="clear-filters">
              Limpar Filtros
            </button>
          </div>
        )}
      </aside>

      <TagsFilterModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        tags={tags}
        selectedTags={selectedTags}
        onTagToggle={onTagToggle}
      />
    </>
  )
}
