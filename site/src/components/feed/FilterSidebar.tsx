import { useState } from "react"
import TagsFilterModal from "../../components/feed/TagsFilterModal"
import "./FilterSidebar.css"

interface Tag {
  id: string
  label: string
}

interface FilterSidebarProps {
  tags: Tag[]
  selectedTags: string[]
  onTagToggle: (tagId: string) => void
  selectedCategory: string
  onCategoryChange: (category: string) => void
}

export default function FilterSidebar({
  tags,
  selectedTags,
  onTagToggle,
  selectedCategory,
  onCategoryChange,
}: FilterSidebarProps) {
  const [isModalOpen, setIsModalOpen] = useState(false)

  const categories = [
    { id: "Todos", label: "Todos" },
    { id: "Laboratórios", label: "Laboratórios" },
    { id: "Equipe de Competição", label: "Equipe de Competição" },
    { id: "Empresas Juniores", label: "Empresas Juniores" },
  ]

  return (
    <>
      <aside className="filter-sidebar">
        <div className="filter-header">
          <svg className="filter-icon" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 5h14M5 10h10M7 15h6" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
          <h2 className="filter-title">Filtros</h2>
        </div>

        <div className="filter-section">
          <h3 className="filter-section-title">CATEGORIAS</h3>
          <div className="filter-options">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => onCategoryChange(category.id)}
                className={`filter-button ${selectedCategory === category.id ? "active" : ""}`}
              >
                {category.label}
              </button>
            ))}
          </div>
        </div>

        <div className="filter-section">
          <h3 className="filter-section-title">TAGS</h3>
          <button 
            onClick={() => setIsModalOpen(true)} 
            className="tags-filter-button bg-primary"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2 4h12M4 8h8M6 12h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            Selecionar Tags
            {selectedTags.length > 0 && (
              <span className="tags-count">{selectedTags.length}</span>
            )}
          </button>
        </div>

        {selectedTags.length > 0 && (
          <div className="selected-tags">
            <h3 className="filter-section-title">TAGS SELECIONADAS</h3>
            <div className="tags-list">
              {selectedTags.map((tagId) => {
                const tag = tags.find((t) => t.id === tagId)
                return tag ? (
                  <span key={tagId} className="tag-badge">
                    {tag.label}
                    <button onClick={() => onTagToggle(tagId)} className="tag-remove">
                      ×
                    </button>
                  </span>
                ) : null
              })}
            </div>
            <button onClick={() => selectedTags.forEach(onTagToggle)} className="clear-filters">
              Limpar Tags
            </button>
          </div>
        )}

        <div className="filter-tip">
          <div className="tip-label">💡 Dica</div>
          <div className="tip-text">
            Clique em uma oportunidade para ver todos os detalhes!
          </div>
        </div>
      </aside>

      <TagsFilterModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        tags={tags}
        selectedTags={selectedTags}
        onTagToggle={onTagToggle}
        onSave={(newSelectedTags) => {
          // Zera todas as tags selecionadas
          selectedTags.forEach(tag => {
            if (!newSelectedTags.includes(tag)) {
              onTagToggle(tag) // desmarca se não está mais
            }
          })
        
          // Marca as novas que não estavam antes
          newSelectedTags.forEach(tag => {
            if (!selectedTags.includes(tag)) {
              onTagToggle(tag)
            }
          })
        }}
      />
    </>
  )
}
