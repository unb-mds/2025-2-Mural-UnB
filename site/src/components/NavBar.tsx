import React, { useState, useEffect, useRef } from "react"
import { fetchOpportunitiesFromJSON, type Opportunity } from "data/fetchOpportunities"
import Logo from "assets/images/MuralLogo_M.svg"
import { Link, useLocation } from "react-router-dom"

const Navbar: React.FC = () => {
  const location = useLocation()
  const [input, setInput] = useState("")
  const [isSearchFocused, setIsSearchFocused] = useState(false)
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetchOpportunitiesFromJSON()
      .then((opps) => setOpportunities(opps))
      .catch((error) => console.error("Erro ao buscar oportunidades:", error))
  }, [])

  // Fechar menu ao clicar fora
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsMenuOpen(false)
      }
    }
    
    if (isMenuOpen) {
      document.addEventListener("mousedown", handleClickOutside)
    }
    
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [isMenuOpen])

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

  const navLinks = [
    { to: "/", label: "Home" },
    { to: "/feed", label: "Mural" },
    { to: "/about", label: "Sobre" },
    { to: "https://tiagosbittencourt.github.io/Mural-UnB/", label: "Docs", external: true },
  ]

  return (
    <div className="navbar bg-base-100 shadow-sm relative px-4 lg:pr-10">
      <div className="navbar-start">
        {/* Menu Hamburger - Mobile */}
        <div className="dropdown lg:hidden" ref={menuRef}>
          <button
            className="btn btn-ghost"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Menu"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              {isMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
          
          {isMenuOpen && (
            <ul className="menu menu-sm dropdown-content mt-3 z-[100] p-2 shadow-lg bg-base-100 rounded-box w-52 border border-gray-200">
              {navLinks.map((link) => (
                <li key={link.to}>
                  <Link
                    to={link.to}
                    className={`font-gowunBold py-3 transition-all duration-200 hover:text-primary hover:bg-primary/10 border-l-2 border-transparent hover:border-secondary ${location.pathname === link.to ? "bg-primary/10 text-primary border-l-2 border-secondary" : ""}`}
                    onClick={() => setIsMenuOpen(false)}
                    {...(link.external ? { target: "_blank", rel: "noopener noreferrer" } : {})}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>

        <Link to="/feed">
          <img 
            src={Logo || "/placeholder.svg"} 
            className="w-20 h-10 lg:w-30 lg:h-15 m-2 lg:m-3.5 cursor-pointer" 
            alt="Logo"
          />
        </Link>

        {/* Links de navegação - Desktop */}
        <div className="hidden lg:flex items-center">
          <Link
            to="/"
            className={`text-lg btn-link font-gowunBold ml-8 mr-4 no-underline text-inherit relative pb-1 transition-all duration-200 hover:text-primary after:content-[''] after:absolute after:left-0 after:bottom-0 after:h-[2px] after:bg-secondary after:transition-all after:duration-200 ${location.pathname === "/" ? "text-primary after:w-full" : "after:w-0 hover:after:w-full"}`}
          >
            Home
          </Link>

          <Link
            to="/feed"
            className={`text-lg btn-link font-gowunBold mx-4 no-underline text-inherit relative pb-1 transition-all duration-200 hover:text-primary after:content-[''] after:absolute after:left-0 after:bottom-0 after:h-[2px] after:bg-secondary after:transition-all after:duration-200 ${location.pathname === "/feed" ? "text-primary after:w-full" : "after:w-0 hover:after:w-full"}`}
          >
            Mural
          </Link>

          <Link
            to="/about"
            className={`text-lg btn-link font-gowunBold mx-4 no-underline text-inherit relative pb-1 transition-all duration-200 hover:text-primary after:content-[''] after:absolute after:left-0 after:bottom-0 after:h-[2px] after:bg-secondary after:transition-all after:duration-200 ${location.pathname === "/about" ? "text-primary after:w-full" : "after:w-0 hover:after:w-full"}`}
          >
            Sobre
          </Link>

          <Link
            to="https://tiagosbittencourt.github.io/Mural-UnB/"
            className={`text-lg btn-link font-gowunBold mx-4 no-underline text-inherit relative pb-1 transition-all duration-200 hover:text-primary after:content-[''] after:absolute after:left-0 after:bottom-0 after:h-[2px] after:w-0 after:bg-secondary after:transition-all after:duration-200 hover:after:w-full`}
            target="_blank"
            rel="noopener noreferrer"
          >
            Docs
          </Link>
        </div>
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
              className="input input-bordered input-base-300 w-40 sm:w-48 md:w-64 pr-10 focus:outline-none text-sm"
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
            <div className="absolute top-12 right-0 bg-white shadow-lg rounded-lg p-2 z-50 w-56 sm:w-64 max-h-60 overflow-y-auto border border-gray-200">
              <div className="text-xs text-gray-500 mb-2 font-medium">
                {filteredOpportunities.length} oportunidade{filteredOpportunities.length !== 1 ? 's' : ''} encontrada{filteredOpportunities.length !== 1 ? 's' : ''}
              </div>
              
              {filteredOpportunities.length > 0 ? (
                <ul className="space-y-1">
                  {filteredOpportunities.map((opportunity) => (
                    <li key={opportunity.id}>
                      <Link 
                        to={`/feed/${opportunity.id}`}
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