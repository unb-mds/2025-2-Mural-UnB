import { useState, useMemo, useEffect } from "react"
import type { Opportunity } from "../../data/opportunities"
import { opportunities as staticOpportunities } from "../../data/opportunities"
import { getAllTagsFlat } from "../../data/tags"
import type { Tag } from "../../data/tags"
import FilterSidebar from "../../components/feed/FilterSidebar"
import OpportunityCard from "../../components/feed/OpportunityCard"
import { fetchOpportunitiesFromJSON } from "../../data/fetchOpportunities"
import { fetchTagsFlat } from "../../data/fetchTags"
import "./FeedPage.css"

export default function FeedPage() {
  // Carregar tags salvas do localStorage ao iniciar
  const loadSavedTags = (): string[] => {
    try {
      const saved = localStorage.getItem('selectedTags')
      if (saved) {
        const parsed = JSON.parse(saved)
        return Array.isArray(parsed) ? parsed : []
      }
    } catch (error) {
      console.error('Erro ao carregar tags do localStorage:', error)
    }
    return []
  }

  const [searchTerm, setSearchTerm] = useState("")
  const [selectedTags, setSelectedTags] = useState<string[]>(loadSavedTags())
  const [selectedCategory, setSelectedCategory] = useState<string>("Todos")
  const [fetchedOpportunities, setFetchedOpportunities] = useState<Opportunity[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [allTagsFetched, setAllTagsFetched] = useState<Tag[] | null>(null)

  // Carregar oportunidades e tags do JSON público
  useEffect(() => {
    let mounted = true
    Promise.all([fetchOpportunitiesFromJSON(), fetchTagsFlat()])
      .then(([opps, tags]) => {
        if (!mounted) return
        setFetchedOpportunities(opps)
        // Se tags.json falhar ou vier vazio
        setAllTagsFetched(tags.length > 0 ? tags : null)
        setIsLoading(false)
      })
      .catch(() => {
        if (!mounted) return
        setAllTagsFetched(null)
        setIsLoading(false)
      })
    return () => { mounted = false }
  }, [])

  const allTags = useMemo(() => allTagsFetched ?? getAllTagsFlat(), [allTagsFetched])

  // Combinar oportunidades do fetch com oportunidades estáticas
  const allOpportunities = useMemo(() => {
    const fetchedIds = new Set(fetchedOpportunities.map(opp => opp.id))
    const staticOnly = staticOpportunities.filter(opp => !fetchedIds.has(opp.id))
    return [...fetchedOpportunities, ...staticOnly]
  }, [fetchedOpportunities])

  const filteredOpportunities = useMemo(() => {
    return allOpportunities.filter((opp) => {
      const matchesSearch =
        searchTerm === "" ||
        opp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        opp.shortDescription.toLowerCase().includes(searchTerm.toLowerCase())

      const matchesTags =
        selectedTags.length === 0 ||
        (opp.tags && selectedTags.every((tagId) => opp.tags?.includes(tagId)))

      return matchesSearch && matchesTags
    })
  }, [searchTerm, selectedTags, allOpportunities])

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
            {isLoading ? (
              <div className="no-results">
                <p>Carregando oportunidades...</p>
              </div>
            ) : filteredByCategory.length > 0 ? (
              filteredByCategory.map((opportunity) => (
                <OpportunityCard
                  key={opportunity.id}
                  opportunity={{
                    id: opportunity.id,
                    title: opportunity.name,
                    description: opportunity.shortDescription,
                    date: "",
                    location: "",
                    tags: opportunity.tags || [],
                    link: `/Mural/${opportunity.id}`,
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

