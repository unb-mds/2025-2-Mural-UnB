import { useState } from "react"
import TagsFilterModal from "./TagsFilterModal"

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
      <aside className="bg-white rounded-xl p-6 h-fit sticky top-[90px] border border-[#e5e5e5] max-lg:static">
        {/* Header */}
        <div className="flex items-center gap-2 mb-6">
          <svg className="text-[#1a7f4e]" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 5h14M5 10h10M7 15h6" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
          <h2 className="text-xl font-bold text-[#1a1a1a]">Filtros</h2>
        </div>

        {/* Categories Section */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-[#666] mb-3 uppercase tracking-[0.5px]">CATEGORIAS</h3>
          <div className="flex flex-col gap-2">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => onCategoryChange(category.id)}
                className={`py-3 px-4 border-none rounded-lg text-left text-base cursor-pointer transition-all duration-200 font-medium ${
                  selectedCategory === category.id 
                    ? "bg-[#1a7f4e] text-white" 
                    : "bg-[#f5f5f5] text-[#333] hover:bg-[#e5e5e5]"
                }`}
              >
                {category.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tags Section */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-[#666] mb-3 uppercase tracking-[0.5px]">TAGS</h3>
          <button 
            onClick={() => setIsModalOpen(true)} 
            className="w-full flex items-center justify-center gap-2 py-3 px-4 border-none rounded-lg text-base font-semibold text-white cursor-pointer transition-all duration-200 relative bg-primary hover:-translate-y-0.5 hover:shadow-[0_4px_12px_rgba(147,51,234,0.3)]"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2 4h12M4 8h8M6 12h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            Selecionar Tags
            {selectedTags.length > 0 && (
              <span className="absolute -top-1.5 -right-1.5 bg-[#ef4444] text-white text-xs font-bold py-0.5 px-1.5 rounded-[10px] min-w-[20px] text-center">
                {selectedTags.length}
              </span>
            )}
          </button>
        </div>

        {/* Selected Tags */}
        {selectedTags.length > 0 && (
          <div className="flex flex-col gap-2 mt-3">
            <h3 className="text-sm font-semibold text-[#666] mb-3 uppercase tracking-[0.5px]">TAGS SELECIONADAS</h3>
            <div className="flex flex-col gap-2">
              {selectedTags.map((tagId) => {
                const tag = tags.find((t) => t.id === tagId)
                return tag ? (
                  <span key={tagId} className="flex items-center justify-between py-2 px-3 bg-[#f0f9f4] border border-[#b8e6d0] rounded-md text-sm text-[#15663e] font-medium">
                    {tag.label}
                    <button 
                      onClick={() => onTagToggle(tagId)} 
                      className="bg-transparent border-none cursor-pointer p-1 text-[#1a7f4e] flex items-center justify-center transition-colors duration-200 hover:text-[#15663e]"
                    >
                      ×
                    </button>
                  </span>
                ) : null
              })}
            </div>
            <button 
              onClick={() => selectedTags.forEach(onTagToggle)} 
              className="mt-2 py-2 px-4 bg-[#ef4444] text-white border-none rounded-lg text-sm font-semibold cursor-pointer transition-all duration-200 hover:bg-[#dc2626]"
            >
              Limpar Tags
            </button>
          </div>
        )}

        {/* Tip */}
        <div className="bg-[#f0f9f4] rounded-lg p-4 border-l-[3px] border-[#1a7f4e] mt-6">
          <div className="font-semibold text-[#1a7f4e] mb-1 text-sm">💡 Dica</div>
          <div className="text-sm text-[#666] leading-6">
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
