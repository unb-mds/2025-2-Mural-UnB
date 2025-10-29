import { Phone, Mail, Fan as Fax, Instagram } from "lucide-react"
import "./Footer.css"

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        {/* Left Section - Organization Info */}
        <div className="footer-section">
          <h2 className="footer-org-name">Mural UnB</h2>
          <p className="footer-address">Faculdade de Ciências e Tecnologias em Engenharia</p>
          <p className="footer-address">Brasília - DF, 70910-900</p>
        </div>

        {/* Middle Section - Contact Info */}
        <div className="footer-section footer-contact">
          <div className="footer-contact-item">
            <Phone className="footer-icon" size={18} />
            <span>+55 61 9999999</span>
          </div>
          <div className="footer-contact-item">
            <Phone className="footer-icon" size={18} />
            <span>Estudantes +55 61 9999999</span>
          </div>
          <div className="footer-contact-item">
            <Fax className="footer-icon" size={18} />
            <span>+55 61 99999999</span>
          </div>
          <div className="footer-contact-item">
            <Mail className="footer-icon" size={18} />
            <a href="mailto:contato@muralunb.com" className="footer-email">
              ???@gmail.com
            </a>
          </div>
        </div>

        {/* Right Section - CTA Button */}
        <div className="footer-section footer-cta">
          <a href="#contato" className="footer-button">
            CONTATO & SUPORTE
          </a>
        </div>
      </div>

      {/* Bottom Section - Social Media & Links */}
      <div className="footer-bottom">
        <div className="footer-bottom-content">
          {/* Social Media Icons */}
          <div className="footer-social">
            <a
              href="https://instagram.com/muralunb"
              target="_blank"
              rel="noopener noreferrer"
              className="footer-social-link"
            >
              <Instagram size={20} />
            </a>
          </div>

          {/* Navigation Links */}
          <nav className="footer-nav">
            <a href="/" className="footer-link">
              Feed
            </a>
            <a href="#sobre" className="footer-link">
              Sobre
            </a>
          </nav>

          {/* Logo/Badge */}
          <div className="footer-badge">
            <img src="/mural-unb-logo.png" alt="Mural UnB" className="footer-logo" />
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
