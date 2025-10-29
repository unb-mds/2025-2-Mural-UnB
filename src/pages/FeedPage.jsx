"use client"

import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { opportunities } from "../data/opportunities"
import FilterSidebar from "../components/FilterSidebar"
import OpportunityCard from "../components/OpportunityCard"
import "./FeedPage.css"

function FeedPage() {
  const [selectedCategory, setSelectedCategory] = useState("Todos")
  const navigate = useNavigate()

  const filteredOpportunities =
    selectedCategory === "Todos" ? opportunities : opportunities.filter((opp) => opp.category === selectedCategory)

  const handleCardClick = (id) => {
    navigate(`/oportunidade/${id}`)
  }

  return (
    <div className="feed-page">
      <div className="feed-container">
        <div className="feed-main">
          <div className="feed-header">
            <h1 className="feed-title">Oportunidades na UnB</h1>
            <p className="feed-subtitle">Descubra laboratórios, equipes competitivas e empresas juniores!</p>
          </div>

          <div className="opportunities-grid">
            {filteredOpportunities.map((opportunity) => (
              <OpportunityCard
                key={opportunity.id}
                opportunity={opportunity}
                onClick={() => handleCardClick(opportunity.id)}
              />
            ))}
          </div>
        </div>

        <FilterSidebar selectedCategory={selectedCategory} onCategoryChange={setSelectedCategory} />
      </div>
    </div>
  )
}

export default FeedPage
