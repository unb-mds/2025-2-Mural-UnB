import { useState, useMemo } from "react"
import { opportunities } from "../../data/opportunities"
import { getAllTagsFlat } from "../../data/tags"
import FilterSidebar from "../../components/feed/FilterSidebar"
import OpportunityCard from "../../components/feed/OpportunityCard"
import "./FeedPage.css"

export default function FeedPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>("Todos")
  const allTags = getAllTagsFlat()

  const filteredOpportunities = useMemo(() => {
    return opportunities.filter((opp) => {
      // Filtrar por termo de busca
      const matchesSearch =
        searchTerm === "" ||
        opp.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        opp.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        opp.name.toLowerCase().includes(searchTerm.toLowerCase())

      // Filtrar por tags
      const matchesTags =
        selectedTags.length === 0 ||
        selectedTags.every((tagId) => opp.tags.includes(tagId))

      return matchesSearch && matchesTags
    })
  }, [searchTerm, selectedTags])

  const handleTagToggle = (tagId: string) => {
    setSelectedTags((prev) =>
      prev.includes(tagId) ? prev.filter((id) => id !== tagId) : [...prev, tagId]
    )
  }

  const filteredByCategory = useMemo(() => {
    if (selectedCategory === "Todos") {
      return filteredOpportunities
    }
    return filteredOpportunities.filter((opp) => opp.category === selectedCategory)
  }, [filteredOpportunities, selectedCategory])

  return (
    <div className="feed-page">
      <div className="feed-container">
        <main className="feed-main">
          <div className="feed-header">
            <h1>Oportunidades na UnB</h1>
            <p className="feed-subtitle">
              Descubra laboratórios, equipes competitivas e empresas juniores!
            </p>
          </div>

          <div className="opportunities-list">
            {filteredByCategory.length > 0 ? (
              filteredByCategory.map((opportunity) => (
                <OpportunityCard
                  key={opportunity.id}
                  opportunity={{
                    id: opportunity.id,
                    title: opportunity.title,
                    description: opportunity.description,
                    date: opportunity.date,
                    location: opportunity.location,
                    tags: opportunity.tags,
                    link: `/Oportunidades/${opportunity.id}`,
                    logo: opportunity.logo
                  }}
                />
              ))
            ) : (
              <div className="no-results">
                <p>Nenhuma oportunidade encontrada com os filtros selecionados.</p>
                <button
                  onClick={() => {
                    setSearchTerm("")
                    setSelectedTags([])
                    setSelectedCategory("Todos")
                  }}
                  className="clear-filters-button"
                >
                  Limpar Filtros
                </button>
              </div>
            )}
          </div>
        </main>

        <FilterSidebar
          tags={allTags}
          selectedTags={selectedTags}
          onTagToggle={handleTagToggle}
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
        />
      </div>
    </div>
  )
}

