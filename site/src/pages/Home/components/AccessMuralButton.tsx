import { Link } from "react-router-dom"

const AccessMuralButton = () => {
  return (
    <Link to="/feed" className="w-full px-4 sm:px-6 flex justify-center mt-6 sm:mt-10 mb-6 sm:mb-8">
      <button className="group relative btn btn-primary px-10 sm:px-14 md:px-16 py-3 sm:py-5 md:py-7 rounded-full w-full max-w-sm sm:max-w-md md:max-w-lg shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 overflow-hidden">
        {/* Efeito de brilho no hover */}
        <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></span>
        
        <span className="relative flex items-center gap-2 sm:gap-3 text-lg sm:text-xl md:text-2xl lg:text-3xl font-bold">
          Acesse o Mural
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className="h-5 w-5 sm:h-6 sm:w-6 md:h-7 md:w-7 group-hover:translate-x-1 transition-transform duration-300" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" >
            </path>
          </svg>
        </span>
      </button>
    </Link>
  )
}

export default AccessMuralButton
