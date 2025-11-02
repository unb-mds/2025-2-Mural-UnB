import { Phone, Mail, Fan as Fax, Instagram } from "lucide-react"
import "./Footer.css"

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h2 className="footer-org-name">Mural UnB</h2>
          <p className="footer-address">Faculdade de Ciências e Tecnologias em Engenharia</p>
          <p className="footer-address">Brasília - DF, 70910-900</p>
        </div>

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

        <div className="footer-section footer-cta">
          <a href="#contato" className="footer-button">
            CONTATO & SUPORTE
          </a>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="footer-bottom-content">
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

          <nav className="footer-nav">
            <a href="/Oportunidades" className="footer-link">
              Oportunidades
            </a>
            <a href="#sobre" className="footer-link">
              Sobre
            </a>
          </nav>

          <div className="footer-badge">
            <img src="/mural-unb-logo.png" alt="Mural UnB" className="footer-logo" />
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
