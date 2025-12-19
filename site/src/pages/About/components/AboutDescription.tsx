
const AboutDescription = () => {
  return (
    <section className="max-w-3xl mx-auto bg-base-100 rounded-xl drop-shadow-xl mb-10 px-6 py-8 flex flex-col gap-4">
      <h2 className="text-2xl md:text-3xl font-gowunBold text-primary mb-2">Por que criamos o Mural UnB?</h2>
      <p className="text-base md:text-lg text-gray-700 leading-relaxed">
        Durante nossa trajetória na UnB/FGA, sentimos na pele a dificuldade de encontrar informações sobre oportunidades, eventos e atividades extracurriculares. Tudo estava espalhado em grupos, planilhas, murais físicos e sites diferentes. Isso dificultava o acesso e fazia muitos estudantes perderem chances valiosas.
      </p>
      <p className="text-base md:text-lg text-gray-700 leading-relaxed">
        O <span className="font-bold text-primary">Mural UnB</span> nasceu para resolver esse problema: centralizar, organizar e facilitar o acesso a tudo que pode impulsionar sua vida acadêmica e profissional.
      </p>
      <ul className="list-disc pl-6 text-base md:text-lg text-gray-700 leading-relaxed mb-2">
        <li><span className="font-semibold text-secondary">Busca inteligente</span> com IA para recomendar oportunidades alinhadas ao seu perfil.</li>
        <li><span className="font-semibold text-secondary">Tags e filtros</span> para você encontrar rapidamente o que procura.</li>
        <li><span className="font-semibold text-secondary">Interface intuitiva</span> e responsiva, feita por e para estudantes.</li>
      </ul>
      <p className="text-base md:text-lg text-gray-700 leading-relaxed">
        Nosso objetivo é que nenhum talento da FGA perca oportunidades por falta de informação. O Mural UnB é feito por alunos, para alunos - e está em constante evolução!
      </p>
    </section>
  )
}

export default AboutDescription
