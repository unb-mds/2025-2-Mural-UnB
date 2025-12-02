import React, { useState, useEffect } from "react"
import { fetchOpportunitiesFromJSON, type Opportunity } from "data/fetchOpportunities"
import Logo from "assets/images/MuralLogo_M.svg"
import { Link, useLocation } from "react-router-dom"

const Navbar: React.FC = () => {
  const location = useLocation()
  const [input, setInput] = useState("")
  const [isSearchFocused, setIsSearchFocused] = useState(false)
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])

  useEffect(() => {
    fetchOpportunitiesFromJSON()
      .then((opps) => setOpportunities(opps))
      .catch((error) => console.error("Erro ao buscar oportunidades:", error))
  }, [])

  const filteredOpportunities = opportunities.filter(opp =>
    opp.name.toLowerCase().includes(input.toLowerCase())
  ).slice(0, 10) // Mostra apenas os top 10

  const highlightMatch = (name: string, searchTerm: string) => {
    if (!searchTerm) return name
    
    const lowerName = name.toLowerCase()
    const lowerSearch = searchTerm.toLowerCase()
    const matchIndex = lowerName.indexOf(lowerSearch)
    
    if (matchIndex === -1) return name
    
    const beforeMatch = name.slice(0, matchIndex)
    const match = name.slice(matchIndex, matchIndex + searchTerm.length)
    const afterMatch = name.slice(matchIndex + searchTerm.length)
    
    return (
      <>
        {beforeMatch}
        <mark className="bg-secondary/60 rounded px-0.5">{match}</mark>
        {afterMatch}
      </>
    )
  }

  return (
    <div className="navbar bg-base-100 shadow-sm relative pr-10">
      <div className="navbar-start">
        <img 
          src={Logo || "/placeholder.svg"} 
          className="w-30 h-15 m-3.5" 
          alt="Logo"
        />

        <Link
          to="/2025-2-Mural-UnB/"
          className={`btn-lg btn-link font-gowunBold mr-5 ml-10 no-underline text-inherit hover:no-underline hover:text-inherit ${location.pathname === "/2025-2-Mural-UnB/" ? "btn-active" : ""}`}
        >
          Home
        </Link>

        <Link
          to="/2025-2-Mural-UnB/Sobre"
          className={`btn-lg btn-link font-gowunBold mr-5 ml-5 no-underline text-inherit hover:no-underline hover:text-inherit ${location.pathname === "/2025-2-Mural-UnB/Sobre" ? "btn-active" : ""}`}
        >
          Sobre
        </Link>

        <Link
          to="/2025-2-Mural-UnB/feed"
          className={`btn-lg btn-link font-gowunBold ml-5 no-underline text-inherit hover:no-underline hover:text-inherit ${location.pathname === "/2025-2-Mural-UnB/feed" ? "btn-active" : ""}`}
        >
          Mural
        </Link>
      </div>

      <div className="navbar-end">
        <div className="relative">
          <div className="flex items-center">
            <input 
              type="text" 
              placeholder="Pesquisar"
              value={input} 
              onChange={(e) => setInput(e.target.value)}
              onFocus={() => setIsSearchFocused(true)}
              onBlur={() => setTimeout(() => setIsSearchFocused(false), 200)}
              className="input input-bordered input-base-300 w-32 md:w-64 pr-10 focus:outline-none"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 absolute right-3 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>

          {/* Dropdown de Resultados da Busca*/}
          {(input && isSearchFocused) && (
            <div className="absolute top-12 right-0 bg-white shadow-lg rounded-lg p-2 z-50 w-64 max-h-60 overflow-y-auto border border-gray-200">
              <div className="text-xs text-gray-500 mb-2 font-medium">
                {filteredOpportunities.length} oportunidade{filteredOpportunities.length !== 1 ? 's' : ''} encontrada{filteredOpportunities.length !== 1 ? 's' : ''}
              </div>
              
              {filteredOpportunities.length > 0 ? (
                <ul className="space-y-1">
                  {filteredOpportunities.map((opportunity) => (
                    <li key={opportunity.id}>
                      <Link 
                        to={`/2025-2-Mural-UnB/feed/${opportunity.id}`}
                        className="flex items-center p-2 hover:bg-gray-100 rounded-md no-underline text-inherit transition-colors"
                        onClick={() => setInput("")}
                      >
                        {opportunity.logo && (
                          <img 
                            src={opportunity.logo} 
                            alt={opportunity.name}
                            className="w-6 h-6 mr-2 rounded"
                          />
                        )}
                        <span className="text-sm">
                          {highlightMatch(opportunity.name, input)}
                        </span>
                      </Link>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="p-2 text-gray-500 text-sm text-center">
                  Sem resultados para "{input}"
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Navbar