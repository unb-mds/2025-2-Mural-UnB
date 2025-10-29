"use client"

import { useParams, useNavigate } from "react-router-dom"
import { opportunities } from "../data/opportunities"
import "./DetailPage.css"

function DetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const opportunity = opportunities.find((opp) => opp.id === id)

  if (!opportunity) {
    return (
      <div className="detail-page">
        <div className="detail-container">
          <p>Oportunidade não encontrada</p>
          <button onClick={() => navigate("/")}>Voltar ao Feed</button>
        </div>
      </div>
    )
  }

  return (
    <div className="detail-page">
      <div className="detail-container">
        <button className="back-button" onClick={() => navigate("/")}>
          ← Voltar ao Feed
        </button>

        {opportunity.coverImage && (
          <div className="cover-image">
            <img src={opportunity.coverImage || "/placeholder.svg"} alt={opportunity.name} />
          </div>
        )}

        <div className="detail-header">
          <div className="detail-logo-container">
            <img
              src={opportunity.logo || "/placeholder.svg"}
              alt={`${opportunity.name} logo`}
              className="detail-logo"
            />
          </div>
          <div className="detail-title-section">
            <h1 className="detail-title">{opportunity.name}</h1>
            <p className="detail-subtitle">{opportunity.shortDescription}</p>
          </div>
          <div className="detail-actions">
            {opportunity.social?.instagram && (
              <a
                href={opportunity.social.instagram}
                target="_blank"
                rel="noopener noreferrer"
                className="social-button"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" />
                </svg>
              </a>
            )}
            {opportunity.social?.website && (
              <a href={opportunity.social.website} target="_blank" rel="noopener noreferrer" className="social-button">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10" strokeWidth="2" />
                  <path
                    d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
                    strokeWidth="2"
                  />
                </svg>
              </a>
            )}
          </div>
        </div>

        <div className="detail-content">
          {opportunity.about && (
            <section className="detail-section">
              <h2 className="section-title">Sobre:</h2>
              <p className="section-text">{opportunity.about}</p>
            </section>
          )}

          {opportunity.mission && (
            <section className="detail-section">
              <h2 className="section-title">Missão:</h2>
              <p className="section-text">{opportunity.mission}</p>
            </section>
          )}

          {opportunity.vision && (
            <section className="detail-section">
              <h2 className="section-title">Visão:</h2>
              <p className="section-text">{opportunity.vision}</p>
            </section>
          )}

          {opportunity.values && (
            <section className="detail-section">
              <h2 className="section-title">Valores:</h2>
              <p className="section-text">{opportunity.values}</p>
            </section>
          )}

          {opportunity.services && (
            <section className="detail-section">
              <h2 className="section-title">Serviços:</h2>
              <p className="section-text">{opportunity.services}</p>
            </section>
          )}
        </div>
      </div>
    </div>
  )
}

export default DetailPage
