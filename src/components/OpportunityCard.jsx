"use client"

import "./OpportunityCard.css"

function OpportunityCard({ opportunity, onClick }) {
  return (
    <div className="opportunity-card" onClick={onClick}>
      <div className="card-content">
        <div className="card-logo-container">
          <img src={opportunity.logo || "/placeholder.svg"} alt={`${opportunity.name} logo`} className="card-logo" />
        </div>
        <div className="card-info">
          <h3 className="card-title">{opportunity.name}</h3>
          <p className="card-description">{opportunity.shortDescription}</p>
        </div>
      </div>
    </div>
  )
}

export default OpportunityCard
