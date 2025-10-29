"use client"

import "./FilterSidebar.css"

const categories = ["Todos", "Laboratórios", "Equipes Competitivas", "Empresas Juniores"]

function FilterSidebar({ selectedCategory, onCategoryChange }) {
  return (
    <aside className="filter-sidebar">
      <div className="filter-header">
        <svg className="filter-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path
            d="M2.5 5.83333H17.5M5.83333 10H14.1667M8.33333 14.1667H11.6667"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
        <h2 className="filter-title">Filtros</h2>
      </div>

      <div className="filter-section">
        <h3 className="filter-section-title">Categorias</h3>
        <div className="filter-options">
          {categories.map((category) => (
            <button
              key={category}
              className={`filter-button ${selectedCategory === category ? "active" : ""}`}
              onClick={() => onCategoryChange(category)}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-tip">
        <p className="tip-label">Dica:</p>
        <p className="tip-text">Clique em uma oportunidade para ver todos os detalhes!</p>
      </div>
    </aside>
  )
}

export default FilterSidebar
