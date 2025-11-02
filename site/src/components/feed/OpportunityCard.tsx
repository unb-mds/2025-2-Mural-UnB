
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
  // Criar um placeholder de logo baseado no nome
  const getLogoPlaceholder = () => {
    const initial = opportunity.title.charAt(0).toUpperCase()
    return (
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '2rem',
        fontWeight: 'bold',
        color: '#1a7f4e',
        background: '#f0f9f4'
      }}>
        {initial}
      </div>
    )
  }

  return (
    <Link to={`/Oportunidades/${opportunity.id}`} className="opportunity-card">
      <div className="card-logo">
        {opportunity.logo ? (
          <img 
            src={opportunity.logo} 
            alt={`${opportunity.title} logo`}
            onError={(e) => {
              const target = e.currentTarget
              target.style.display = 'none'
              const placeholder = target.parentElement?.querySelector('.logo-placeholder') as HTMLElement
              if (placeholder) {
                placeholder.style.display = 'flex'
              }
            }}
          />
        ) : null}
        {!opportunity.logo && (
          <div className="logo-placeholder">
            {getLogoPlaceholder()}
          </div>
        )}
      </div>
      
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
