import { useParams, Link } from "react-router-dom"
import { useState, useEffect, useMemo } from "react"
import type { Opportunity } from "../../data/fetchOpportunities"
import { fetchOpportunitiesFromJSON } from "../../data/fetchOpportunities"

function resolveHeaderImage(id: string, name: string): string | null {
  if (!id && !name) return null
  
  const base = import.meta.env.BASE_URL || '/'
  const resolvePath = (path: string) => base.endsWith('/') ? `${base}${path.slice(1)}` : `${base}${path}`
  
  const idMap: { [key: string]: { headerName: string, ejId: string } } = {
    "ej-100022": { headerName: "engnet", ejId: "100022" },
    "ej-100021": { headerName: "enetec", ejId: "100021" },
    "ej-100019": { headerName: "embragea", ejId: "100019" },
    "ej-100018": { headerName: "eletrojun", ejId: "100018" },
  }
  
  if (id && idMap[id]) {
    const { headerName } = idMap[id]
    return resolvePath(`/images/headers/${headerName}.png`)
  }
  
  const n = name?.toLowerCase().trim() || ""
  
  const nameMap: { [key: string]: string } = {
    "engnet": "engnet.png",
    "enetec": "enetec.png",
    "embragea": "embragea.png",
    "eletronjun": "eletrojun.png",
    "eletrojun": "eletrojun.png",
    "cjr": "cjr.png",
    "apuama": "apuama.png",
    "unball": "unball.png",
    "unbeatables": "unbeatables.jpg",
    "unbeattles": "unbeattles.jpg",
    "draco": "draco.png",
    "piratas": "piratas.png",
    "engrena": "engrena.png",
    "aess": "aess.png",
    "ailab": "ailab.png",
    "matriz": "matriz.png",
    "ai lab": "ailab.png",
    "comsoc": "comsoc.png",
    "cs": "cs.png",
    "struct": "struct.png",
    "labmicro": "labmicro.png",
    "edra": "edra.png",
    "labtelecom/lcept": "labtelecom.png",
    "gmec": "GMEC.png",
    "lappis": "lappis.png",
    "capital rocket": "rocketcapital.png",
    "cedis": "cedis.png",
    "rocket capital": "rocketcapital.png",
    "rocket team": "rocketcapital.png",
    "cenia": "cenia.png",
    "mamutes": "MAMUTES.png",
    "mecajun": "mecajun.png",
    "droid": "droid.png",
    "titans": "titans.png",
    "computational intelligence": "cis-ieee.jpg",
    "cis": "cis-ieee.jpg",
    "nanotec": "NANOTEC.png",
    "itrac": "itrac.png",
    "circuit": "cas.png",
    "o2": "o2.png",
    "orc": "orc.png",
    "unbaja": "unbaja.png",
    "lara": "lara.png",
    "orc'estra": "orc.png",
    "woman": "woman-engineering.png",
    "orcestra": "orc.png",
    "tecmec": "TECMEC.png",
  }
  
  for (const [key, filename] of Object.entries(nameMap)) {
    if (n.includes(key)) {
      return resolvePath(`/images/headers/${filename}`)
    }
  }
  
  return null
}

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
      <div className="max-w-[1200px] mx-auto p-8 min-h-[calc(100vh-80px)] max-md:p-4">
        <div className="text-center py-16 px-8">
          <h1 className="text-[2rem] text-[#1a1a1a] mb-4">Carregando...</h1>
        </div>
      </div>
    )
  }

  if (!opportunity) {
    return (
      <div className="max-w-[1200px] mx-auto p-8 min-h-[calc(100vh-80px)] max-md:p-4">
        <div className="text-center py-16 px-8">
          <h1 className="text-[2rem] text-[#1a1a1a] mb-4">Oportunidade não encontrada</h1>
          <Link to="/" className="inline-flex items-center gap-2 text-[#1a7f4e] no-underline font-semibold mb-8 transition-colors hover:text-[#15663e]">
            Voltar para oportunidades
          </Link>
        </div>
      </div>
    )
  }

  const headerImage = resolveHeaderImage(opportunity.id, opportunity.name)

  return (
    <div className="max-w-[1200px] mx-auto p-8 min-h-[calc(100vh-80px)] max-md:p-4">
      <Link to="/feed" className="inline-flex items-center gap-2 text-[#1a7f4e] no-underline font-semibold mb-8 transition-colors hover:text-[#15663e]">
        ← Voltar
      </Link>

      {headerImage ? (
        <div className="w-full h-[400px] overflow-hidden rounded-t-xl mb-0 bg-[#003366] relative max-md:h-[250px] max-md:rounded-t-lg">
          <img 
            src={headerImage} 
            alt={`${opportunity.name} header`}
            className="w-full h-full object-cover block"
            onError={(e) => {
              const img = e.currentTarget
              const src = img.getAttribute('src') || ''
              
              if (src.includes('/images/ejs/') || !src.includes('/images/headers/')) {
                const parent = img.parentElement
                if (parent) {
                  parent.className = 'w-full h-[400px] bg-[#003366] rounded-t-xl mb-0 max-md:h-[250px] max-md:rounded-t-lg'
                  img.style.display = 'none'
                }
                return
              }
              
              const ejId = opportunity.id.replace('ej-', '')
              if (ejId) {
                const base = import.meta.env.BASE_URL || '/'
                const resolvePath = (path: string) => base.endsWith('/') ? `${base}${path.slice(1)}` : `${base}${path}`
                const ejPath = resolvePath(`/images/ejs/${ejId}.jpeg`)
                img.src = ejPath
              } else {
                const parent = img.parentElement
                if (parent) {
                  parent.className = 'w-full h-[400px] bg-[#003366] rounded-t-xl mb-0 max-md:h-[250px] max-md:rounded-t-lg'
                  img.style.display = 'none'
                }
              }
            }}
          />
        </div>
      ) : (
        <div className="w-full h-[400px] bg-[#003366] rounded-t-xl mb-0 max-md:h-[250px] max-md:rounded-t-lg"></div>
      )}

      <article className="bg-white rounded-b-xl p-8 border border-[#e5e5e5] border-t-0 shadow-md mt-0 max-md:p-6 max-md:rounded-b-lg">
        <header className="text-center mb-8 pb-8 border-b border-[#e5e5e5]">
          {opportunity.logo && (
            <div className="w-[120px] h-[120px] mx-auto mb-6 rounded-xl overflow-hidden bg-[#f5f5f5] flex items-center justify-center">
              <img src={opportunity.logo} alt={opportunity.name} className="w-full h-full object-cover" />
            </div>
          )}
          <h1 className="text-[2.5rem] font-bold text-[#1a1a1a] m-0 mb-2 max-md:text-[2rem]">{opportunity.name}</h1>
          
          
          <p className="text-base text-[#1a7f4e] font-semibold uppercase tracking-wide mb-4">
            {opportunity.category}
            {opportunity.campus && opportunity.campus !== "N/A" && (
              <span className="opacity-90 font-normal">
                {' • '}{opportunity.campus}
              </span>
            )}
          </p>

          <p className="text-lg text-[#666] leading-relaxed m-0">{opportunity.shortDescription}</p>
        </header>

        {opportunity.tags && opportunity.tags.length > 0 && (
          <div className="flex flex-wrap gap-3 mb-8 pb-8 border-b border-[#e5e5e5]">
            {opportunity.tags.map((tag) => (
              <span key={tag} className="inline-block py-2 px-4 bg-[#f0f9f4] border border-[#b8e6d0] rounded-[20px] text-sm text-[#15663e] font-medium">
                {tag.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        )}

        <div className="leading-[1.8] text-[#333]">
          {opportunity.about && (
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-[#1a1a1a] mb-4 pb-2 border-b-2 border-[#e5e5e5]">Sobre</h2>
              <p className="text-lg text-[#666] leading-[1.8] m-0">{opportunity.about}</p>
            </section>
          )}

          {opportunity.mission && (
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-[#1a1a1a] mb-4 pb-2 border-b-2 border-[#e5e5e5]">Missão</h2>
              <p className="text-lg text-[#666] leading-[1.8] m-0">{opportunity.mission}</p>
            </section>
          )}

          {opportunity.vision && (
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-[#1a1a1a] mb-4 pb-2 border-b-2 border-[#e5e5e5]">Visão</h2>
              <p className="text-lg text-[#666] leading-[1.8] m-0">{opportunity.vision}</p>
            </section>
          )}

          {opportunity.values && (
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-[#1a1a1a] mb-4 pb-2 border-b-2 border-[#e5e5e5]">Valores</h2>
              <p className="text-lg text-[#666] leading-[1.8] m-0">{opportunity.values}</p>
            </section>
          )}

          {opportunity.services && (
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-[#1a1a1a] mb-4 pb-2 border-b-2 border-[#e5e5e5]">Serviços</h2>
              <p className="text-lg text-[#666] leading-[1.8] m-0">{opportunity.services}</p>
            </section>
          )}
        </div>

        {opportunity.social && (
          <footer className="flex gap-4 mt-8 pt-8 border-t border-[#e5e5e5] justify-center max-md:flex-col">
            {opportunity.social.website && (
              <a
                href={opportunity.social.website}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center py-3 px-8 bg-[#1a7f4e] text-white no-underline rounded-lg font-semibold transition-all border-none cursor-pointer text-base min-w-[44px] min-h-[44px] hover:bg-[#15663e] hover:-translate-y-0.5 hover:shadow-[0_4px_12px_rgba(26,127,78,0.3)] max-md:w-full"
              >
                Visitar Site
              </a>
            )}
            {opportunity.social.instagram && (
              <a
                href={opportunity.social.instagram}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center py-3 px-8 bg-white text-[#1a7f4e] no-underline rounded-lg font-semibold transition-all border-2 border-[#1a7f4e] cursor-pointer text-base min-w-[44px] min-h-[44px] hover:bg-[#f0f9f4] max-md:w-full [&:has(svg:only-child)]:p-3 [&:has(svg:only-child)]:w-[44px]"
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
