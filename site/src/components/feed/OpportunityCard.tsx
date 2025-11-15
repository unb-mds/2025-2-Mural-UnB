
import { Link } from "react-router-dom"
import "./OpportunityCard.css"

interface Opportunity {
  id: string
  title: string
  description: string
  date: string
  location: string
  tags: string[]
  link: string
  logo?: string
}

interface OpportunityCardProps {
  opportunity: Opportunity
}

export default function OpportunityCard({ opportunity }: OpportunityCardProps) {
  return (
    <Link to={`/Oportunidades/${opportunity.id}`} className="opportunity-card">
      {opportunity.logo && (
        <div className="card-logo">
          <img 
            src={opportunity.logo} 
            alt={`${opportunity.title} logo`}
          />
        </div>
      )}
      
      <div className="card-content">
        <div className="card-header">
          <h3 className="card-title">{opportunity.title}</h3>
        </div>

        <p className="card-description">{opportunity.description}</p>

        <div className="card-tags">
          {opportunity.tags.slice(0, 2).map((tag) => (
            <span key={tag} className="tag">
              {tag.replace(/_/g, " ")}
            </span>
          ))}
          {opportunity.tags.length > 2 && <span className="tag-more">+{opportunity.tags.length - 2}</span>}
        </div>
      </div>
    </Link>
  )
}
