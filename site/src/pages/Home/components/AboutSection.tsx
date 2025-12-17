const AboutSection = () => {
  return (
    <div className="flex flex-col items-center gap-6 mt-10">
      <h1 className="text-4xl font-bold mb-2">Sobre Nós</h1>

      <div className="rounded-xl p-6 bg-base-100 flex flex-col items-center text-center w-234 drop-shadow-md">
        <h1 className="text-2xl font-gowunBold mb-2">Quem somos?</h1>
        <h2 className="whitespace-normal wrap-break-words text-base">
          O Mural UnB é uma plataforma digital projetada para centralizar e recomendar oportunidades acadêmicas e profissionais dentro da Universidade de Brasília (UnB).
        </h2>
      </div>

      <div className="flex flex-row gap-10">
        <div className="rounded-xl p-6 bg-base-100 flex flex-col items-center text-center max-w-md drop-shadow-md">
          <h1 className="text-2xl font-gowunBold mb-2">Objetivo?</h1>
          <h2 className="whitespace-normal wrap-break-words text-base">
            O objetivo é criar uma experiência personalizada, onde os estudantes possam facilmente descobrir oportunidades alinhadas aos seus interesses e histórico acadêmico.
          </h2>
        </div>

        <div className="rounded-xl p-6 bg-base-100 flex flex-col items-center text-center max-w-md drop-shadow-md">
          <h1 className="text-2xl font-gowunBold mb-2">Como?</h1>
          <h2 className="whitespace-normal wrap-break-words text-base">
            Analisamos os interesses e preferências do usuário utilizando machine learning para recomendar as opções mais relevantes e enviar notificações sobre novas oportunidades.
          </h2>
        </div>
      </div>
    </div>
  )
}

export default AboutSection
