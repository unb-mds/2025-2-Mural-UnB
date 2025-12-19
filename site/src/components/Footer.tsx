import { Link } from "react-router-dom"
import LogoUnB from "assets/images/logo-unb-branco.png"

function Footer() {
  return (
    <footer className="bg-[#2e8b57] text-white px-4 sm:px-8 pt-8 pb-4">
      {/* Content */}
      <div className="max-w-[1400px] mx-auto grid grid-cols-1 sm:grid-cols-2 gap-8 sm:gap-12 mb-6">
        {/* Left Section */}
        <div className="flex flex-col gap-5 items-center sm:items-start">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <img src="/MuralLogo_S.svg" alt="Mural UnB" className="w-12 h-12 brightness-0 invert" />
            <span className="text-2xl font-bold text-white">Mural UnB</span>
          </div>

          {/* Contact */}
          <div className="flex flex-col gap-2 items-center sm:items-start">
            <h3 className="text-lg font-bold text-white m-0">Contate-nos</h3>
            <p className="text-sm text-white/90 m-0 leading-6">unb.mural@gmail.com</p>
            <p className="text-sm text-white/90 m-0 leading-6">+55 61 9 91231231</p>
          </div>

          {/* Social */}
          <div className="flex gap-4 mt-2">
            <a
              href="https://instagram.com/muralunb"
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 border-2 border-white rounded-full flex items-center justify-center text-white no-underline transition-all duration-200 hover:bg-white hover:text-[#2e8b57] hover:-translate-y-0.5"
              aria-label="Instagram"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path 
                  d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" 
                  fill="currentColor"
                />
              </svg>
            </a>
            <a
              href="https://github.com/unb-mds/2025-2-Mural-UnB"
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 border-2 border-white rounded-full flex items-center justify-center text-white no-underline transition-all duration-200 hover:bg-white hover:text-[#2e8b57] hover:-translate-y-0.5"
              aria-label="GitHub"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path 
                  d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" 
                  fill="currentColor"
                />
              </svg>
            </a>
          </div>
        </div>

        {/* Right Section */}
        <div className="flex flex-col gap-4 items-center sm:items-start">
          <h3 className="text-2xl font-bold text-white m-0">Páginas</h3>
          <nav className="flex flex-col gap-3 items-center sm:items-start">
            <Link to="/" className="text-white no-underline text-base font-medium transition-all duration-200 hover:opacity-80 hover:translate-x-1">Home</Link>
            <Link to="/about" className="text-white no-underline text-base font-medium transition-all duration-200 hover:opacity-80 hover:translate-x-1">Sobre</Link>
            <Link to="/feed" className="text-white no-underline text-base font-medium transition-all duration-200 hover:opacity-80 hover:translate-x-1">Mural</Link>
            <Link to="https://tiagosbittencourt.github.io/Mural-UnB/" className="text-white no-underline text-base font-medium transition-all duration-200 hover:opacity-80 hover:translate-x-1">Docs</Link>
          </nav>
        </div>
      </div>

      {/* Bottom */}
      <div className="max-w-[1400px] mx-auto pt-6">
        <div className="w-full h-px bg-white/30 mb-4"></div>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-8">
          <img src={LogoUnB} alt="Universidade de Brasília" className="h-4 sm:h-5" />
          <p className="text-center text-xs sm:text-sm text-white/80 m-0">© 2025 Mural UnB. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
