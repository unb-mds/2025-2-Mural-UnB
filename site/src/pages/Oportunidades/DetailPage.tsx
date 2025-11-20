import { useParams, Link } from "react-router-dom"
import { useState, useEffect, useMemo } from "react"
import type { Opportunity } from "../../data/fetchOpportunities"
import { fetchOpportunitiesFromJSON } from "../../data/fetchOpportunities"
import "./DetailPage.css"

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
    return (
      <div className="detail-container">
        <div className="not-found">
          <h1>Carregando...</h1>
        </div>
      </div>
    )
  }

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
          {opportunity.logo && (
            <div className="detail-logo">
              <img src={opportunity.logo} alt={opportunity.name} />
            </div>
          )}
          <h1>{opportunity.name}</h1>
          <p className="detail-category">{opportunity.category}</p>
          <p className="detail-short-description">{opportunity.shortDescription}</p>
        </header>

        {opportunity.tags && opportunity.tags.length > 0 && (
          <div className="detail-tags">
            {opportunity.tags.map((tag) => (
              <span key={tag} className="tag">
                {tag.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        )}

        <div className="detail-description">
          {opportunity.about && (
            <section>
              <h2>Sobre</h2>
              <p>{opportunity.about}</p>
            </section>
          )}

          {opportunity.mission && (
            <section>
              <h2>Missão</h2>
              <p>{opportunity.mission}</p>
            </section>
          )}

          {opportunity.vision && (
            <section>
              <h2>Visão</h2>
              <p>{opportunity.vision}</p>
            </section>
          )}

          {opportunity.values && (
            <section>
              <h2>Valores</h2>
              <p>{opportunity.values}</p>
            </section>
          )}

          {opportunity.services && (
            <section>
              <h2>Serviços</h2>
              <p>{opportunity.services}</p>
            </section>
          )}
        </div>

        {opportunity.social && (
          <footer className="detail-footer">
            {opportunity.social.website && (
              <a
                href={opportunity.social.website}
                target="_blank"
                rel="noopener noreferrer"
                className="apply-button"
              >
                Visitar Site
              </a>
            )}
            {opportunity.social.instagram && (
              <a
                href={opportunity.social.instagram}
                target="_blank"
                rel="noopener noreferrer"
                className="apply-button secondary"
                aria-label="Instagram"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"
                    fill="currentColor"
                  />
                </svg>
              </a>
            )}
          </footer>
        )}
      </article>
    </div>
  )
}


