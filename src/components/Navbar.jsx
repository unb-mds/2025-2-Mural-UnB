import { Link } from "react-router-dom"

function Navbar() {
  return (
    <div className="navbar bg-[#003d82] text-white shadow-lg">
      <div className="navbar-start">
        <div className="dropdown">
          <div tabIndex={0} role="button" className="btn btn-ghost lg:hidden">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h8m-8 6h16" />
            </svg>
          </div>
          <ul
            tabIndex={0}
            className="menu menu-sm dropdown-content bg-white text-gray-800 rounded-box z-[1] mt-3 w-52 p-2 shadow"
          >
            <li>
              <Link to="/">Feed</Link>
            </li>
            <li>
              <a href="#sobre">Sobre</a>
            </li>
            <li>
              <a href="#contato">Contato</a>
            </li>
          </ul>
        </div>
        <Link to="/" className="btn btn-ghost text-xl hover:bg-[#00508f]">
          <img src="/images/mural-unb-logo.png" alt="Mural UnB" className="h-8 w-8" />
          <span className="hidden sm:inline">Mural UnB</span>
        </Link>
      </div>
      <div className="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal px-1">
          <li>
            <Link to="/" className="hover:bg-[#00508f]">
              Feed
            </Link>
          </li>
          <li>
            <a href="#sobre" className="hover:bg-[#00508f]">
              Sobre
            </a>
          </li>
          <li>
            <a href="#contato" className="hover:bg-[#00508f]">
              Contato
            </a>
          </li>
        </ul>
      </div>
      <div className="navbar-end">
        <a
          href="https://instagram.com"
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-ghost btn-circle hover:bg-[#00508f]"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
            <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
            <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
          </svg>
        </a>
      </div>
    </div>
  )
}

export default Navbar