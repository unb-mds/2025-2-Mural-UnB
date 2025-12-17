interface FeedHeaderProps {
  hasRecommendations: boolean
}

const FeedHeader = ({ hasRecommendations }: FeedHeaderProps) => {
  return (
    <div className="flex flex-col gap-2">
      <h1 className="text-[2rem] font-bold text-[#1a1a1a] m-0">
        Oportunidades na UnB
      </h1>
      <p className="text-[#666] text-base">
        {hasRecommendations
          ? "Recomendadas para você com base nos seus interesses."
          : "Explorar todas as oportunidades (A-Z)"}
      </p>
    </div>
  )
}

export default FeedHeader
