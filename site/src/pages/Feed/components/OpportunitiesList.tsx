import OpportunityCard from "../../../components/feed/OpportunityCard"
import type { Opportunity } from "../../../data/fetchOpportunities"

interface OpportunityWithScore extends Opportunity {
  score?: number
}

interface OpportunitiesListProps {
  opportunities: OpportunityWithScore[]
}

const OpportunitiesList = ({ opportunities }: OpportunitiesListProps) => {
  return (
    <>
      {opportunities.map((opportunity) => (
        <OpportunityCard
          key={opportunity.id}
          opportunity={{
            id: opportunity.id,
            title: opportunity.name,
            description: opportunity.shortDescription,
            date: "",
            location: "",
            tags: opportunity.tags || [],
            link: `/feed/${opportunity.id}`,
            logo: opportunity.logo,
          }}
        />
      ))}
    </>
  )
}

export default OpportunitiesList
