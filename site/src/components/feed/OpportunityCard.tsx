
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
}

interface OpportunityCardProps {
  opportunity: Opportunity
}

export default function OpportunityCard({ opportunity }: OpportunityCardProps) {
  return (
    <Link to={`/Oportunidades/${opportunity.id}`} className="opportunity-card">
      <div className="card-header">
        <h3 className="card-title">{opportunity.title}</h3>
        <span className="card-date">{opportunity.date}</span>
      </div>

      <p className="card-description">{opportunity.description}</p>

      <div className="card-footer">
        <span className="card-location">{opportunity.location}</span>
        <div className="card-tags">
          {opportunity.tags.slice(0, 3).map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
          {opportunity.tags.length > 3 && <span className="tag-more">+{opportunity.tags.length - 3}</span>}
        </div>
      </div>
    </Link>
  )
}
