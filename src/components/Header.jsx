import { Link } from "react-router-dom"
import "./Header.css"

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="logo-link">
          <img src="/mural-unb-logo.png" alt="Mural UnB" className="logo" />
        </Link>
        <nav className="nav">
          <Link to="/" className="nav-link">
            Feed
          </Link>
          <a href="#sobre" className="nav-link">
            Home
          </a>
        </nav>
      </div>
    </header>
  )
}

export default Header
