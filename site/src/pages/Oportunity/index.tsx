import { useParams, Link } from "react-router-dom"
import { useState, useEffect, useMemo } from "react"
import type { Opportunity } from "../../data/fetchOpportunities"
import { fetchOpportunitiesFromJSON } from "../../data/fetchOpportunities"
import { resolveHeaderImage } from "./utils/resolveHeaderImage"
import {
  LoadingState,
  NotFoundState,
  HeaderImage,
  OpportunityHeader,
  TagsList,
  DescriptionSections,
  SocialFooter,
} from "./components"

export default function DetailPage() {
  const { id } = useParams<{ id: string }>()
  const [allOpportunities, setAllOpportunities] = useState<Opportunity[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    fetchOpportunitiesFromJSON()
      .then((opps) => {
        if (!mounted) return
        setAllOpportunities(opps)
        setIsLoading(false)
      })
      .catch((error) => {
        console.error("Erro ao buscar oportunidades:", error)
        if (!mounted) return
        setIsLoading(false)
      })
    return () => {
      mounted = false
    }
  }, [])

  const opportunity = useMemo(
    () => allOpportunities.find((opp) => opp.id === id),
    [allOpportunities, id]
  )

  if (isLoading) {
    return <LoadingState />
  }

  if (!opportunity) {
    return <NotFoundState />
  }

  const headerImage = resolveHeaderImage(opportunity.id, opportunity.name)

  return (
    <div className="max-w-[1200px] mx-auto p-8 min-h-[calc(100vh-80px)] max-md:p-4">
      <Link
        to="/feed"
        className="inline-flex items-center gap-2 text-[#1a7f4e] no-underline font-semibold mb-8 transition-colors hover:text-[#15663e]"
      >
        ← Voltar
      </Link>

      <HeaderImage
        imageUrl={headerImage}
        name={opportunity.name}
        opportunityId={opportunity.id}
      />

      <article className="bg-white rounded-b-xl p-8 border border-[#e5e5e5] border-t-0 shadow-md mt-0 max-md:p-6 max-md:rounded-b-lg">
        <OpportunityHeader
          logo={opportunity.logo}
          name={opportunity.name}
          category={opportunity.category}
          campus={opportunity.campus}
          shortDescription={opportunity.shortDescription}
        />

        <TagsList tags={opportunity.tags || []} />

        <DescriptionSections
          about={opportunity.about}
          mission={opportunity.mission}
          vision={opportunity.vision}
          values={opportunity.values}
          services={opportunity.services}
        />

        <SocialFooter
          website={opportunity.social?.website}
          instagram={opportunity.social?.instagram}
        />
      </article>
    </div>
  )
}
