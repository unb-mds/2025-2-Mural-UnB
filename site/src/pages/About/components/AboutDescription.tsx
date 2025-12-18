const AboutDescription = () => {
  return (
    <div className="max-w-3xl mx-auto flex flex-row gap-10 p-5 bg-base-100 rounded-xl drop-shadow-xl mb-10">
      <div>
        <p className="font-gowunBold text-lg md:text-xl wrap-break-words leading-relaxed md:leading-loose mb-2">
          Como alunos da UnB no campus da FGA, percebemos que não existia um
          ambiente que centralizasse informações sobre atividades extras. A
          busca por diferentes tipos de eventos ou detalhes era complicada, com
          materiais dispersos em diversos arquivos e sites.
        </p>
      </div>
      <div>
        <p className="font-gowunBold text-lg md:text-xl wrap-break-words leading-relaxed md:leading-loose">
          Nasceu assim o <strong className="text-primary">Mural UnB</strong>,
          nosso projeto da disciplina de Métodos de Desenvolvimento de Software.
          É uma plataforma intuitiva que simplifica a busca por atividades e
          oportunidades, utilizando{" "}
          <strong className="text-secondary">IA para organização</strong>,
          sistema de{" "}
          <strong className="text-secondary">tags categorizadas</strong> e uma
          <strong className="text-secondary"> ferramenta de pesquisa</strong>.
        </p>
      </div>
    </div>
  )
}

export default AboutDescription
