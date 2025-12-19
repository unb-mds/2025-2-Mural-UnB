import { DevelopersGrid } from "./components"

export default function Sobre() {
  return (
    <div className="flex flex-col items-center gap-8 py-6 px-2 sm:px-4">
      {/* Box: Sobre o Mural UnB */}
      <div className="rounded-2xl p-4 sm:p-6 md:p-8 bg-base-100 flex flex-col items-center text-center w-full max-w-5xl shadow-md hover:shadow-xl transition-shadow duration-300 border-t-4 border-primary">
        <h2 className="text-2xl sm:text-3xl font-gowunBold mb-3 text-primary">Sobre o Mural UnB</h2>
        <p className="text-base sm:text-lg text-gray-600 leading-relaxed">
          O Mural UnB é uma plataforma digital criada para centralizar e recomendar oportunidades acadêmicas e extracurriculares dentro da Universidade de Brasília (UnB), especialmente no campus FGA. Nosso objetivo é facilitar o acesso dos estudantes a eventos, projetos, laboratórios, empresas juniores e equipes de competição, utilizando inteligência artificial, tags inteligentes e uma interface intuitiva.
        </p>
      </div>

      {/* Box: Sobre a Equipe */}
      <div className="rounded-2xl p-4 sm:p-6 md:p-8 bg-base-100 flex flex-col items-center text-center w-full max-w-5xl shadow-md hover:shadow-xl transition-shadow duration-300 border-t-4 border-secondary">
        <h2 className="text-2xl sm:text-3xl font-gowunBold mb-3 text-secondary">Sobre a Equipe</h2>
        <p className="text-base sm:text-lg text-gray-600 leading-relaxed">
          O projeto é desenvolvido por um time multidisciplinar de estudantes da FGA, apaixonados por tecnologia, design, dados e educação. Cada integrante contribuiu com sua expertise para criar uma solução inovadora, aberta e colaborativa para toda a comunidade acadêmica da UnB.
        </p>
      </div>

      {/* Grid de desenvolvedores */}
      <DevelopersGrid />
    </div>
  )
}
