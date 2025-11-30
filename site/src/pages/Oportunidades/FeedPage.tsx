import { useState, useMemo, useEffect } from "react"

import type { Opportunity } from "../../data/fetchOpportunities"
import { fetchOpportunitiesFromJSON } from "../../data/fetchOpportunities"
import { fetchTagsFlat } from "../../data/fetchTags"
import { getAllTagsFlat } from "../../data/tags"
import type { Tag } from "../../data/tags"

import FilterSidebar from "../../components/feed/FilterSidebar"
import OpportunityCard from "../../components/feed/OpportunityCard"

import { cosineSimilarity, calculateMeanVector } from "../../utils/vectorMatch"

import "./FeedPage.css"

interface OpportunityWithScore extends Opportunity {
  score?: number; 
}

export default function Feed() {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedTags, setSelectedTags] = useState<string[]>([]) 
  const [selectedCategory, setSelectedCategory] = useState<string>("Todos")
  
  const [fetchedOpportunities, setFetchedOpportunities] = useState<OpportunityWithScore[]>([])
  const [allTagsFetched, setAllTagsFetched] = useState<Tag[] | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  
  const [userEmbedding, setUserEmbedding] = useState<number[] | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 8

  useEffect(() => {
    let mounted = true
    Promise.all([fetchOpportunitiesFromJSON(), fetchTagsFlat()])
      .then(([opps, tags]) => {
        if (!mounted) return
        setFetchedOpportunities(opps)
        setAllTagsFetched(tags.length > 0 ? tags : null)
        setIsLoading(false)
      })
      .catch((error) => {
        console.error("Erro ao carregar dados:", error)
        if (!mounted) return
        setIsLoading(false)
      })
    return () => { mounted = false }
  }, [])
  
  useEffect(() => {
    if (!allTagsFetched) return;

    if (selectedTags.length > 0) {

      const selectedTagObjects = allTagsFetched.filter(tag => 
        selectedTags.includes(tag.id) && tag.embedding
      );

      const vectors = selectedTagObjects.map(t => t.embedding!);

      if (vectors.length > 0) {
        const meanVector = calculateMeanVector(vectors);
        
        setUserEmbedding(meanVector);
        localStorage.setItem("userMeanEmbedding", JSON.stringify(meanVector));
      }
    } else {
      setUserEmbedding(null);
      localStorage.removeItem("userMeanEmbedding");
    }
  }, [selectedTags, allTagsFetched]);

  const allTags = useMemo(() => allTagsFetched ?? getAllTagsFlat(), [allTagsFetched])

  const displayedOpportunities = useMemo(() => {
    
    const opportunitiesWithScores = fetchedOpportunities.map((opp) => {
      let score = 0;
      
      if (userEmbedding && userEmbedding.length > 0 && opp.embedding && opp.embedding.length > 0) {
        try {
           score = cosineSimilarity(userEmbedding, opp.embedding);
        } catch (err) {
           console.warn("Erro matemático no calculo de similaridade", err);
           score = 0;
        }
      }
      
      return { ...opp, score };
    });

    const filtered = opportunitiesWithScores.filter((opp) => {
      const matchesSearch =
        searchTerm === "" ||
        opp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        opp.shortDescription.toLowerCase().includes(searchTerm.toLowerCase())

      const matchesCategory =
        selectedCategory === "Todos" || opp.category === selectedCategory

      return matchesSearch && matchesCategory
    })

    const sorted = [...filtered];

    if (userEmbedding) {
      sorted.sort((a, b) => (b.score || 0) - (a.score || 0));
    } else {
      sorted.sort((a, b) => a.name.localeCompare(b.name));
    }

    const startIndex = (currentPage - 1) * itemsPerPage
    const endIndex = startIndex + itemsPerPage
    const paginatedItems = sorted.slice(startIndex, endIndex)
    const totalPages = Math.ceil(sorted.length / itemsPerPage)

    return {
      items: paginatedItems,
      totalItems: sorted.length,
      totalPages
    };
  }, [searchTerm, selectedCategory, fetchedOpportunities, userEmbedding, currentPage])

  const handleTagToggle = (tagId: string) => {
    setSelectedTags((prev) => {
      const newTags = prev.includes(tagId) ? prev.filter((id) => id !== tagId) : [...prev, tagId];
      
      localStorage.setItem("selectedTags", JSON.stringify(newTags));
      
      if (newTags.length === 0) {
        localStorage.removeItem("userMeanEmbedding");
        window.dispatchEvent(new Event("storage"));
      }
      
      return newTags;
    })
    setCurrentPage(1)
  }

  useEffect(() => {
    setCurrentPage(1)
  }, [searchTerm, selectedCategory])

  return (
    <div className="feed-page">
      <div className="feed-container">
        <main className="feed-main">
          <div className="feed-header">
            <h1>Oportunidades na UnB</h1>
            <p className="feed-subtitle">
              {userEmbedding 
                ? "Recomendadas para você com base nos seus interesses." 
                : "Explorar todas as oportunidades (A-Z)"}
            </p>
          </div>

          <div className="opportunities-list">
            {isLoading ? (
              <div className="no-results"><p>A carregar oportunidades...</p></div>
            ) : displayedOpportunities.items.length > 0 ? (
              displayedOpportunities.items.map((opportunity) => (
                <OpportunityCard
                  key={opportunity.id}
                  opportunity={{
                    id: opportunity.id,
                    title: opportunity.name,
                    description: opportunity.shortDescription,
                    date: "", 
                    location: "",
                    tags: opportunity.tags || [],
                    link: `/Oportunidades/${opportunity.id}`,
                    logo: opportunity.logo,
                  }}
                />
              ))
            ) : (
              <div className="no-results">
                <p>Nenhuma oportunidade encontrada.</p>
                <button 
                  onClick={() => { setSearchTerm(""); setSelectedCategory("Todos"); }}
                  className="clear-filters-button"
                >
                  Limpar Busca
                </button>
              </div>
            )}
          </div>

          {!isLoading && displayedOpportunities.totalPages > 1 && (
            <div className="pagination">
              <button
                className="pagination-btn"
                disabled={currentPage === 1}
                onClick={() => {
                  setCurrentPage(currentPage - 1)
                  window.scrollTo({ top: 0, behavior: 'smooth' })
                }}
              >
                ← Anterior
              </button>

              <div className="pagination-numbers">
                {Array.from({ length: displayedOpportunities.totalPages }, (_, i) => i + 1).map((page) => {
                  const showPage = 
                    page === 1 ||
                    page === displayedOpportunities.totalPages ||
                    Math.abs(page - currentPage) <= 1

                  if (!showPage && page === currentPage - 2) {
                    return <span key={`ellipsis-${page}`} className="pagination-ellipsis">...</span>
                  }
                  
                  if (!showPage && page === currentPage + 2) {
                    return <span key={`ellipsis-${page}`} className="pagination-ellipsis">...</span>
                  }

                  if (!showPage) return null

                  return (
                    <button
                      key={page}
                      className={`pagination-number ${currentPage === page ? "active" : ""}`}
                      onClick={() => {
                        setCurrentPage(page)
                        window.scrollTo({ top: 0, behavior: 'smooth' })
                      }}
                    >
                      {page}
                    </button>
                  )
                })}
              </div>

              <button
                className="pagination-btn"
                disabled={currentPage === displayedOpportunities.totalPages}
                onClick={() => {
                  setCurrentPage(currentPage + 1)
                  window.scrollTo({ top: 0, behavior: 'smooth' })
                }}
              >
                Próxima →
              </button>
            </div>
          )}

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