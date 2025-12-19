import { useSearchParams } from "react-router-dom"
import {
  FeedHeader,
  LoadingState,
  EmptyState,
  Pagination,
  OpportunitiesList,
  FilterSidebar
} from "./components"
import { useFeedData } from "./hooks/useFeedData"

export default function Feed() {
  const [searchParams] = useSearchParams()
  const categoryParam = searchParams.get("category") || undefined
  
  const {
    isLoading,
    allTags,
    selectedTags,
    selectedCategory,
    currentPage,
    userEmbedding,
    displayedOpportunities,
    setSelectedCategory,
    setCurrentPage,
    handleTagToggle,
    clearFilters,
  } = useFeedData(categoryParam)

  return (
    <div className="min-h-[calc(100vh-80px)] p-8 bg-[#f6f6ed] max-md:p-4">
      <div className="max-w-[1400px] mx-auto grid grid-cols-[1fr_300px] gap-8 max-lg:grid-cols-1">
        <main className="flex flex-col gap-8 min-w-0">
          <FeedHeader hasRecommendations={!!userEmbedding} />

          <div className="flex flex-col gap-6">
            {isLoading ? (
              <LoadingState />
            ) : displayedOpportunities.items.length > 0 ? (
              <OpportunitiesList opportunities={displayedOpportunities.items} />
            ) : (
              <EmptyState onClearFilters={clearFilters} />
            )}
          </div>

          {!isLoading && displayedOpportunities.totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={displayedOpportunities.totalPages}
              onPageChange={setCurrentPage}
            />
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