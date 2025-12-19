const AboutSection = () => {
  return (
    <div className="flex flex-col items-center gap-6 sm:gap-8 mt-10 sm:mt-14 px-4 sm:px-6">
      {/* Título com decoração */}
      <div className="flex flex-col items-center gap-2">
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-primary">Sobre Nós</h1>
        <div className="flex items-center gap-2">
          <div className="h-1 w-8 bg-secondary rounded-full"></div>
          <div className="h-1 w-16 bg-primary rounded-full"></div>
          <div className="h-1 w-8 bg-secondary rounded-full"></div>
        </div>
      </div>

      {/* Card principal */}
      <div className="rounded-2xl p-6 sm:p-8 bg-base-100 flex flex-col items-center text-center w-full max-w-5xl shadow-md hover:shadow-xl transition-shadow duration-300 border-t-4 border-primary">
        <h2 className="text-xl sm:text-2xl font-gowunBold mb-3 text-primary">Quem somos?</h2>
        <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
          O Mural UnB é uma plataforma digital projetada para centralizar e recomendar oportunidades acadêmicas e profissionais dentro da Universidade de Brasília (UnB).
        </p>
      </div>

      {/* Cards secundários */}
      <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 md:gap-8 w-full max-w-5xl">
        <div className="rounded-2xl p-5 sm:p-6 bg-base-100 flex flex-col items-center text-center flex-1 shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border-l-4 border-secondary group">
          <h2 className="text-xl sm:text-2xl font-gowunBold mb-3 text-secondary group-hover:text-primary transition-colors duration-300">Objetivo</h2>
          <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
            Criar uma experiência personalizada, onde os estudantes possam facilmente descobrir oportunidades alinhadas aos seus interesses e histórico acadêmico.
          </p>
        </div>

        <div className="rounded-2xl p-5 sm:p-6 bg-base-100 flex flex-col items-center text-center flex-1 shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border-l-4 border-secondary group">
          <h2 className="text-xl sm:text-2xl font-gowunBold mb-3 text-secondary group-hover:text-primary transition-colors duration-300">Como?</h2>
          <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
            Analisamos os interesses e preferências do usuário utilizando machine learning para recomendar as opções mais relevantes e enviar notificações sobre novas oportunidades.
          </p>
        </div>
      </div>
    </div>
  )
}

export default AboutSection
