"use client"

import { useParams, Link } from "react-router-dom"
import { opportunities } from "../../data/opportunities"
import "./DetailPage.css"

export default function DetailPage() {
  const { id } = useParams<{ id: string }>()
  const opportunity = opportunities.find((opp) => opp.id === id)

  if (!opportunity) {
    return (
      <div className="detail-container">
        <div className="not-found">
          <h1>Oportunidade não encontrada</h1>
          <Link to="/Oportunidades" className="back-link">
            Voltar para oportunidades
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="detail-container">
      <Link to="/Oportunidades" className="back-link">
        ← Voltar
      </Link>

      <article className="detail-content">
        <header className="detail-header">
          <h1>{opportunity.title}</h1>
          <div className="detail-meta">
            <span className="detail-date">{opportunity.date}</span>
            <span className="detail-location">{opportunity.location}</span>
          </div>
        </header>

        <div className="detail-tags">
          {opportunity.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>

        <div className="detail-description">
          <p>{opportunity.description}</p>
        </div>

        <footer className="detail-footer">
          <a href={opportunity.link} target="_blank" rel="noopener noreferrer" className="apply-button">
            Candidatar-se
          </a>
        </footer>
      </article>
    </div>
  )
}
