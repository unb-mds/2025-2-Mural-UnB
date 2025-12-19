import { Link } from "react-router-dom"

const InfoBanner = () => {
  const categories = [
    {
      label: "Labs",
      category: "Laboratórios",
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 lg:h-14 lg:w-14 text-primary group-hover:rotate-12 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
        </svg>
      ),
    },
    {
      label: "EJs",
      category: "Empresas Juniores",
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 lg:h-14 lg:w-14 text-primary group-hover:rotate-12 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
    },
    {
      label: "Equipes",
      category: "Equipe de Competição",
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 lg:h-14 lg:w-14 text-primary group-hover:rotate-12 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      ),
    },
  ]

  return (
    <div className="w-full px-4 sm:px-6 mb-10 sm:mb-16 mt-4 sm:mt-6 md:mt-8">
      <div className="max-w-5xl mx-auto bg-base-100 rounded-3xl shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden relative border-t-4 border-primary">
        {/* Decoração de fundo */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full -translate-y-1/2 translate-x-1/2"></div>
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-secondary/5 rounded-full translate-y-1/2 -translate-x-1/2"></div>
        
        <div className="flex flex-col md:flex-row items-center relative z-10">
          {/* Conteúdo */}
          <div className="flex-1 p-8 sm:p-10 md:p-12 lg:p-16 text-center md:text-left">
            <span className="inline-block bg-primary/10 text-primary text-xs sm:text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
              🎓 Para cursos da FGA
            </span>
            <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-primary mb-4 sm:mb-6 leading-tight">
              Todas as oportunidades em um só lugar
            </h2>
            <p className="text-base sm:text-lg md:text-xl text-gray-600 mb-6 sm:mb-8 leading-relaxed max-w-xl">
              Laboratórios, empresas juniores e equipes de competição. 
              Encontre a oportunidade perfeita para a sua carreira!
            </p>
            <Link to="/feed">
              <button className="group bg-primary text-white px-8 sm:px-10 py-4 sm:py-5 rounded-full font-bold text-base sm:text-lg shadow-lg hover:shadow-2xl hover:scale-105 active:scale-95 transition-all duration-300 flex items-center gap-3 mx-auto md:mx-0">
                Explorar oportunidades
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-5 w-5 sm:h-6 sm:w-6 group-hover:translate-x-2 transition-transform duration-300" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </button>
            </Link>
          </div>

          {/* Ícones das categorias com links */}
          <div className="hidden md:flex flex-col gap-4 p-8 lg:p-12">
            {categories.map((cat) => (
              <Link 
                key={cat.category}
                to={`/feed?category=${encodeURIComponent(cat.category)}`}
                className="bg-primary/10 w-24 h-24 lg:w-28 lg:h-28 rounded-2xl hover:bg-primary/20 hover:scale-110 transition-all duration-300 cursor-pointer group flex flex-col items-center justify-center gap-2"
              >
                {cat.icon}
                <p className="text-primary text-xs lg:text-sm font-semibold">{cat.label}</p>
              </Link>
            ))}
          </div>
        </div>

        {/* Ícones mobile */}
        <div className="flex md:hidden justify-center gap-4 pb-8 px-4">
          {categories.map((cat) => (
            <Link 
              key={cat.category}
              to={`/feed?category=${encodeURIComponent(cat.category)}`}
              className="bg-primary/10 w-20 h-20 sm:w-24 sm:h-24 rounded-2xl hover:bg-primary/20 active:scale-95 transition-all duration-300 flex flex-col items-center justify-center gap-1"
            >
              <div className="h-8 w-8 sm:h-10 sm:w-10 text-primary [&>svg]:h-full [&>svg]:w-full">
                {cat.icon}
              </div>
              <p className="text-primary/80 text-[10px] sm:text-xs font-medium">{cat.label}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}

export default InfoBanner
