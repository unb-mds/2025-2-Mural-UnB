export interface Opportunity {
  id: string
  name: string
  title: string
  category: string
  shortDescription: string
  description: string
  date: string
  location: string
  about?: string
  mission?: string
  vision?: string
  values?: string
  services?: string
  tags: string[]
  logo?: string
  coverImage?: string
  social?: {
    website?: string
    instagram?: string
  }
}

export const opportunities: Opportunity[] = [
  {
    id: "orcestra",
    name: "Orc'estra",
    title: "Orc'estra",
    category: "Empresas Juniores",
    shortDescription: "EJ de Engenharia de Software",
    description: "EJ de Engenharia de Software",
    date: "2017",
    location: "UnB - Campus Darcy Ribeiro",
    about:
      "Fundada em 2017, a Empresa Júnior de Engenharia de Software da UnB tem o propósito de ressignificar a vida das pessoas através da gamificação, tornando a vida mais produtiva e prazerosa. O fato curioso é que temos a sede compartilhada com 4 EJs da UnB - UnB. As maiores conquistas foi a empresa, por três anos consecutivos, atingir suas metas e ser considerada uma EJ impactante no Movimento Empresa Júnior. O maior orgulho é pelas conquistas alcançadas até hoje, menos que com pouco tempo de existência já realizamos inúmeros projetos destacáveis, como para a Caixa Seguradora, Vale S.A, PMO Giro Ferentim, entre outras.",
    mission: "Mudar o comportamento das pessoas, através da gamificação, para motivar e engajar nossos parceiros.",
    vision: "Ser referência no Movimento Empresa Júnior apresentando um case de sucesso em até o final de 2025.",
    values: "Sangue Orc, Sintonia, Família e Crescimento.",
    services:
      "Desenvolvimento de software gamificado, aplicativos mobile e web, consultoria em gamificação, design de experiência do usuário.",
    tags: ["desenvolvimento_web", "desenvolvimento_mobile", "desenvolvimento_jogos"],
    logo: "/orc.jpg",
    coverImage: "/orc_equipe.png",
    social: {
      instagram: "https://www.instagram.com/orcgamificacao/",
      website: "https://orcestra.com.br/",
    },
  },
  {
    id: "eletronjun",
    name: "EletroJun",
    title: "EletroJun",
    category: "Empresas Juniores",
    shortDescription: "EJ de Engenharia Eletrônica",
    description: "EJ de Engenharia Eletrônica",
    date: "2020",
    location: "UnB - Campus Darcy Ribeiro",
    about: "...",
    mission:
      "Qualificar os membros através do empreendorismo por meio de soluções em engenharia eletrônica com o objetivo de gerar valor e impacto na sociedade.",
    vision:
      "Ser uma empresa júnior de referência em soluções de engenharia eletrônica no Brasil, materializando ideias com excelência",
    values: "Resiliência, profissionalismo, senso de pertencimento, confiança e aperfeiçoamento.",
    services:
      "Projetos de circuitos analógicos, consultoria, controle eletrônico e monitoramento e transmissão de dados.",
    tags: ["sistemas_embarcados", "circuitos_digitais_analogicos", "eletronica_potencia", "iot"],
    logo: "/eletronjun.png",
    social: {
      instagram: "https://instagram.com/eletronjun",
      website: "https://eletronjun.com.br",
    },
  },
  {
    id: "zenit",
    name: "Zenit Aerospace",
    title: "Zenit Aerospace",
    category: "Empresas Juniores",
    shortDescription: "EJ de Engenharia Aeroespacial",
    description: "EJ de Engenharia Aeroespacial",
    date: "2014",
    location: "UnB - Campus Darcy Ribeiro",
    about:
      "Fundada em 2014, somos uma empresa júnior formada por alunos da UnB, composta por estudantes do curso de Engenharia Aeroespacial. Por isso, a Zenit constitui uma organização sem fins lucrativos regida pela lei 13.267/2016. Comprometidos com a difusão da tecnologia e dos conhecimentos relacionados à imensidão abrigada troposfera acima, somos uma empresa dedicada à inovação do mercado por meio da prestação de serviços de excelência e importância notáveis no ramo aeroespacial. Além disso, possuímos como objetivo o crescimento profissional de nossos membros, tendo em vista capacitações voltadas à inserção no mercado de trabalho. Assim os alunos são responsáveis pelo funcionamento da empresa e possuem autonomia em sua gestão, tendo à sua disposição um conselho formado pelo corpo docente da UnB.",
    mission:
      "Tornar o setor aeroespacial acessível ao cliente por meio de projetos de excelência, proporcionando aos membros vivências empresarial.",
    vision: "Ser referência na expansão do conhecimento aeroespacial no Brasil.",
    values: "Responsabilidade, diversidade, expansão, sempre além.",
    services:
      "Oferecemos os serviços de: curso de pilotagem de drones, modelagem 2D e 3D e consultoria, além do projeto escola espacial.",
    tags: ["vants_drones", "aerodinamica", "sistemas_controle", "modelagem_simulacao_aero"],
    logo: "/zenit.png",
    social: {
      instagram: "https://instagram.com/zenitaerospace",
      website: "https://zenitaerospace.com",
    },
  },
  {
    id: "matriz",
    name: "Matriz",
    title: "Matriz",
    category: "Empresas Juniores",
    shortDescription: "EJ de Engenharia de Energia",
    description: "EJ de Engenharia de Energia",
    date: "2015",
    location: "UnB - Campus Darcy Ribeiro",
    about:
      "A Matriz foi fundado no dia 27 de janeiro de 2015, atuando desde então para diminuir a necessidade do uso de fontes de energia não renováveis, já impactando várias escolas com palestras e workshops e fomos responsáveis pela economia de energia de vários clientes ao longo de nossa história, economia essa que se reflete em mais renda para ele e menos impacto ao meio ambiente.",
    mission:
      "Capacitar membros através da vivência empresarial para impactar a sociedade",
    vision: "Ser reconhecido no mercado, realizando projetos de alto impacto na área energética, formando líderes éticos e conectados",
    values:
      "Vestir a camisa, receptividade, humildade, sinergia e transparência.",
    services: "Fazemos serviços, relacionados a geração e economia de energia, seja ela elétrica ou de outra natureza. Trabalhamos com consultoria em instalação de usinas solares, estudos de eficiência energética, protótipos de economia de energia e temos serviços educacionais, como a escola energética",
    tags: ["energias_renovaveis", "sistemas_eletricos_potencia", "smart_grids", "armazenamento_energia"],
    logo: "/matriz.png",
    social: {
      instagram: "https://instagram.com/matrizenergia",
      website: "https://matrizenergia.com",
    },
  },
  {
    id: "engrena",
    name: "Engrena",
    title: "Engrena",
    category: "Empresas Juniores",
    shortDescription: "EJ de Engenharia Automotiva",
    description: "EJ de Engenharia Automotiva",
    date: "2018",
    location: "UnB - Campus Darcy Ribeiro",
    about:
      "Somos uma Empresa Júnior de Engenharia Automotiva da UnB focada em ser um sistema replicável e sustentável em engenharia automotiva no Brasil, entregando inovação e esclusividade aos nossos clientes. Estudamos, desenvolvemos e geramos soluções para problemas atrelados ao setor automotivo alavancando jovens talentos empreendedores.",
    mission:
      "Estudar, desenvolver e gerar soluções para problemas atrelados ao setor automotivo alavancando jovens talentos empreendedores.",
    vision: "Ser um sistema replicável e sustentável em engenharia automotiva no Brasil, entregando inovação e exclusividade aos nossos clientes",
    services: "Elaboração de laudos técnicos; Consultorias Veicular; Projetos em CAD e CAE; Projetos em impressão 3D; e Cursos voltados para engenharia.",
    tags: ["dinamica_veicular", "sistemas_automotivos", "mobilidade_eletrica", "design_automotivo_cad"],
    logo: "/engrena.png",
    social: {
      instagram: "https://instagram.com/engrenaengenharia",
      website: "https://engrenaengenharia.com",
    },
  },
  {
    id: "cjr",
    name: "CJR",
    title: "CJR",
    category: "Empresas Juniores",
    shortDescription: "EJ de Computação",
    description: "EJ de Computação",
    date: "2010",
    location: "UnB - Campus Darcy Ribeiro",
    about:
      "A CJR é a Empresa Júnior do curso de Ciência da Computação da UnB. Desenvolvemos soluções web e mobile personalizadas para empresas e organizações.",
    mission:
      "Entregar soluções tecnológicas de qualidade enquanto desenvolvemos os melhores profissionais de tecnologia.",
    vision: "Ser referência em desenvolvimento de software no Distrito Federal até 2026.",
    values: "Qualidade, Inovação, Comprometimento e Crescimento Mútuo.",
    services: "Desenvolvimento web, aplicativos mobile, sistemas personalizados, consultoria em TI.",
    tags: ["desenvolvimento_web", "desenvolvimento_mobile", "javascript_ts", "react", "nodejs"],
    logo: "/cjr.png",
    social: {
      instagram: "https://www.instagram.com/cjr.unb/",
      website: "https://www.cjr.org.br/",
    },
  },
]
