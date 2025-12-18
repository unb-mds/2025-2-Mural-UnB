import { Link } from "react-router-dom"
import NotePad from "assets/images/NotePad.png"

const InfoBanner = () => {
  return (
    <div className="flex flex-row items-center justify-center gap-12 py-16 px-8 bg-base-100 rounded-2xl shadow-lg mx-6 mb-12 mt-8">
      <div className="flex-1 max-w-lg">
        <h1 className="text-2xl md:text-2xl leading-relaxed font-gowunBold text-primary">
          Aqui você encontra os detalhes sobre laboratórios, empresas juniores e equipes de competição da UnB-FGA de maneira simplificada e rápida!
        </h1>
      </div>
      <Link to="/feed">
        <div className="flex-shrink-0">
          <img
            src={NotePad}
            alt="Notepad illustration"
            className="w-64 h-auto        drop-shadow-xl"
          />
        </div>
      </Link>
    </div>
  )
}

export default InfoBanner
