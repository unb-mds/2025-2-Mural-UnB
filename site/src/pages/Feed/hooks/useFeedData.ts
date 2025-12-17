import { useState, useEffect, useMemo } from "react"
import type { Opportunity } from "../../../data/fetchOpportunities"
import { fetchOpportunitiesFromJSON } from "../../../data/fetchOpportunities"
import { fetchTagsFlat } from "../../../data/fetchTags"
import { getAllTagsFlat } from "../../../data/tags"
import type { Tag } from "../../../data/tags"
import { cosineSimilarity, calculateMeanVector } from "../../../utils/vectorMatch"

interface OpportunityWithScore extends Opportunity {
  score?: number
}

interface UseFeedDataReturn {
  // State
  isLoading: boolean
  allTags: Tag[]
  selectedTags: string[]
  selectedCategory: string
  searchTerm: string
  currentPage: number
  userEmbedding: number[] | null
  
  // Computed
  displayedOpportunities: {
    items: OpportunityWithScore[]
    totalItems: number
    totalPages: number
  }
  
  // Actions
  setSearchTerm: (term: string) => void
  setSelectedCategory: (category: string) => void
  setCurrentPage: (page: number) => void
  handleTagToggle: (tagId: string) => void
  clearFilters: () => void
}

const ITEMS_PER_PAGE = 8

export function useFeedData(): UseFeedDataReturn {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>("Todos")

  const [fetchedOpportunities, setFetchedOpportunities] = useState<OpportunityWithScore[]>([])
  const [allTagsFetched, setAllTagsFetched] = useState<Tag[] | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const [userEmbedding, setUserEmbedding] = useState<number[] | null>(null)
  const [currentPage, setCurrentPage] = useState(1)

  // Fetch initial data
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
    return () => {
      mounted = false
    }
  }, [])

  // Update user embedding based on selected tags
  useEffect(() => {
    if (!allTagsFetched) return

    if (selectedTags.length > 0) {
      const selectedTagObjects = allTagsFetched.filter(
        (tag) => selectedTags.includes(tag.id) && tag.embedding
      )

      const vectors = selectedTagObjects.map((t) => t.embedding!)

      if (vectors.length > 0) {
        const meanVector = calculateMeanVector(vectors)

        setUserEmbedding(meanVector)
        localStorage.setItem("userMeanEmbedding", JSON.stringify(meanVector))
      }
    } else {
      setUserEmbedding(null)
      localStorage.removeItem("userMeanEmbedding")
    }
  }, [selectedTags, allTagsFetched])

  // Reset page when filters change
  useEffect(() => {
    setCurrentPage(1)
  }, [searchTerm, selectedCategory])

  const allTags = useMemo(
    () => allTagsFetched ?? getAllTagsFlat(),
    [allTagsFetched]
  )

  const displayedOpportunities = useMemo(() => {
    const opportunitiesWithScores = fetchedOpportunities.map((opp) => {
      let score = 0

      if (
        userEmbedding &&
        userEmbedding.length > 0 &&
        opp.embedding &&
        opp.embedding.length > 0
      ) {
        try {
          score = cosineSimilarity(userEmbedding, opp.embedding)
        } catch (err) {
          console.warn("Erro matemático no calculo de similaridade", err)
          score = 0
        }
      }

      return { ...opp, score }
    })

    const filtered = opportunitiesWithScores.filter((opp) => {
      const matchesSearch =
        searchTerm === "" ||
        opp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        opp.shortDescription.toLowerCase().includes(searchTerm.toLowerCase())

      const matchesCategory =
        selectedCategory === "Todos" || opp.category === selectedCategory

      return matchesSearch && matchesCategory
    })

    const sorted = [...filtered]

    if (userEmbedding) {
      sorted.sort((a, b) => (b.score || 0) - (a.score || 0))
    } else {
      sorted.sort((a, b) => a.name.localeCompare(b.name))
    }

    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE
    const endIndex = startIndex + ITEMS_PER_PAGE
    const paginatedItems = sorted.slice(startIndex, endIndex)
    const totalPages = Math.ceil(sorted.length / ITEMS_PER_PAGE)

    return {
      items: paginatedItems,
      totalItems: sorted.length,
      totalPages,
    }
  }, [searchTerm, selectedCategory, fetchedOpportunities, userEmbedding, currentPage])

  const handleTagToggle = (tagId: string) => {
    setSelectedTags((prev) => {
      const newTags = prev.includes(tagId)
        ? prev.filter((id) => id !== tagId)
        : [...prev, tagId]

      localStorage.setItem("selectedTags", JSON.stringify(newTags))

      if (newTags.length === 0) {
        localStorage.removeItem("userMeanEmbedding")
        window.dispatchEvent(new Event("storage"))
      }

      return newTags
    })
    setCurrentPage(1)
  }

  const clearFilters = () => {
    setSearchTerm("")
    setSelectedCategory("Todos")
  }

  return {
    isLoading,
    allTags,
    selectedTags,
    selectedCategory,
    searchTerm,
    currentPage,
    userEmbedding,
    displayedOpportunities,
    setSearchTerm,
    setSelectedCategory,
    setCurrentPage,
    handleTagToggle,
    clearFilters,
  }
}
