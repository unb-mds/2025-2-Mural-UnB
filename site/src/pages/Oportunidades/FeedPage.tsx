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

      const matchesTags =
        selectedTags.length === 0 ||
        (opp.tags && opp.tags.some(tag => selectedTags.includes(tag)))

      return matchesSearch && matchesCategory && matchesTags
    })

    const sorted = [...filtered];

    if (userEmbedding) {
      sorted.sort((a, b) => (b.score || 0) - (a.score || 0));
    } else {
      sorted.sort((a, b) => a.name.localeCompare(b.name));
    }

    return sorted;
  }, [searchTerm, selectedCategory, selectedTags, fetchedOpportunities, userEmbedding])

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
  }

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
            ) : displayedOpportunities.length > 0 ? (
              displayedOpportunities.map((opportunity) => (
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