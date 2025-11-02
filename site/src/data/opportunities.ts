export interface Opportunity {
    id: string
    name: string
    shortDescription: string
    category: string
    logo: string
    tags?: string[]
    coverImage?: string
    about?: string
    mission?: string
    vision?: string
    values?: string
    services?: string
    social?: {
      instagram?: string
      website?: string
    }
  }
  
  export const opportunities: Opportunity[] = [
    {
      id: "Orc'estra Gamificação",
      name: "Orc'estra",
      shortDescription: "EJ de Engenharia de Software",
      category: "Empresas Juniores",
      logo: "/orc.png",
      tags: ["desenvolvimento_web", "desenvolvimento_mobile"],
      coverImage: "/orc_equipe.png",
      about:
        "Fundada em 2017, a Empresa Júnior de Engenharia de Software da UnB tem o propósito de ressignificar a vida das pessoas através da gamificação, tornando a vida mais produtiva e prazerosa. O fato curioso é que temos a sede compartilhada com 4 EJs da UnB - UnB. As maiores conquistas foi a empresa, por três anos consecutivos, atingir suas metas e ser considerada uma EJ impactante no Movimento Empresa Júnior. O maior orgulho é pelas conquistas alcançadas até hoje, menos que com pouco tempo de existência já realizamos inúmeros projetos destacáveis, como para a Caixa Seguradora, Vale S.A, PMO Giro Ferentim, entre outras.",
      mission: "Mudar o comportamento das pessoas, através da gamificação, para motivar e engajar nossos parceiros.",
      vision: "Ser referência no Movimento Empresa Júnior apresentando um case de sucesso em até o final de 2025.",
      values: "Sangue Orc, Sintonia, Família e Crescimento.",
      services:
        "Desenvolvimento de software gamificado, aplicativos mobile e web, consultoria em gamificação, design de experiência do usuário.",
      social: {
        instagram: "https://www.instagram.com/orcgamificacao/",
        website: "https://orcestra.com.br/",
      },
    },
    {
      id: "EletroJun",
      name: "EletroJun",
      shortDescription: "EJ de Engenharia Eletrônica",
      category: "Empresas Juniores",
      logo: "/eletronjun.png",
      tags: ["sistemas_embarcados", "circuitos_digitais_analogicos"],
      about: "...",
      mission:
        "Qualificar os membros através do empreendedorismo por meio de soluções em engenharia eletrônica com o objetivo de gerar valor e impacto na sociedade.",
      vision:
        "Ser uma empresa júnior de referência em soluções de engenharia eletrônica no Brasil, materializando ideias com excelência",
      values: "Resiliência, profissionalismo, senso de pertencimento, confiança e aperfeiçoamento.",
      services:
        "Projetos de circuitos analógicos, consultoria, controle eletrônico e monitoramento e transmissão de dados.",
      social: {
        instagram: "https://instagram.com/eletronjun",
        website: "https://eletronjun.com.br",
      },
    },
    {
      id: "Zenit",
      name: "Zenit Aerospace",
      shortDescription: "EJ de Engenharia Aeroespacial",
      category: "Empresas Juniores",
      logo: "/zenit.png",
      tags: ["vants_drones", "aerodinamica"],
      about:
        "Fundada em 2014, somos uma empresa júnior formada por alunos da UnB, composta por estudantes do curso de Engenharia Aeroespacial. Por isso, a Zenit constitui uma organização sem fins lucrativos regida pela lei 13.267/2016. Comprometidos com a difusão da tecnologia e dos conhecimentos relacionados à imensidão abrigada troposfera acima, somos uma empresa dedicada à inovação do mercado por meio da prestação de serviços de excelência e importância notáveis no ramo aeroespacial. Além disso, possuímos como objetivo o crescimento profissional de nossos membros, tendo em vista capacitações voltadas à inserção no mercado de trabalho. Assim os alunos são responsáveis pelo funcionamento da empresa e possuem autonomia em sua gestão, tendo à sua disposição um conselho formado pelo corpo docente da UnB.",
      mission:
        "Tornar o setor aeroespacial acessível ao cliente por meio de projetos de excelência, proporcionando aos membros vivências empresarial.",
      vision: "Ser referência na expansão do conhecimento aeroespacial no Brasil.",
      values: "Responsabilidade, diversidade, expansão, sempre além.",
      services:
        "Oferecemos os serviços de: curso de pilotagem de drones, modelagem 2D e 3D e consultoria, além do projeto escola espacial.",
      social: {
        instagram: "https://instagram.com/zenitaerospace",
        website: "https://zenitaerospace.com",
      },
    },
    {
      id: "Matriz",
      name: "Matriz",
      shortDescription: "EJ de Engenharia de Energia",
      category: "Empresas Juniores",
      logo: "/matriz.png",
      tags: ["energias_renovaveis", "sistemas_eletricos_potencia"],
      about:
        "A Matriz foi fundado no dia 27 de janeiro de 2015, atuando desde então para diminuir a necessidade do uso de fontes de energia não renováveis, já impactando várias escolas com palestras e workshops e fomos responsáveis pela economia de energia de vários clientes ao longo de nossa história, economia essa que se reflete em mais renda para ele e menos impacto ao meio ambiente.",
      mission: "Capacitar membros através da vivência empresarial para impactar a sociedade",
      vision:
        "Ser reconhecido no mercado, realizando projetos de alto impacto na área energética, formando líderes éticos e conectados",
      values: "Vestir a camisa, receptividade, humildade, sinergia e transparência.",
      services:
        "Fazemos serviços, relacionados a geração e economia de energia, seja ela elétrica ou de outra natureza. Trabalhamos com consultoria em instalação de usinas solares, estudos de eficiência energética, protótipos de economia de energia e temos serviços educacionais, como a escola energética",
      social: {
        instagram: "https://instagram.com/matrizenergia",
        website: "https://matrizenergia.com",
      },
    },
    {
      id: "Engrena",
      name: "Engrena",
      shortDescription: "EJ de Engenharia Automotiva",
      category: "Empresas Juniores",
      logo: "/engrena.png",
      tags: ["dinamica_veicular", "design_automotivo_cad"],
      about:
        "Somos uma Empresa Júnior de Engenharia Automotiva da UnB focada em ser um sistema replicável e sustentável em engenharia automotiva no Brasil, entregando inovação e esclusividade aos nossos clientes. Estudamos, desenvolvemos e geramos soluções para problemas atrelados ao setor automotivo alavancando jovens talentos empreendedores.",
      mission:
        "Estudar, desenvolver e gerar soluções para problemas atrelados ao setor automotivo alavancando jovens talentos empreendedores.",
      vision:
        "Ser um sistema replicável e sustentável em engenharia automotiva no Brasil, entregando inovação e exclusividade aos nossos clientes",
      services:
        "Elaboração de laudos técnicos; Consultorias Veicular; Projetos em CAD e CAE; Projetos em impressão 3D; e Cursos voltados para engenharia.",
      social: {
        instagram: "https://instagram.com/engrenaengenharia",
        website: "https://engrenaengenharia.com",
      },
    },
    {
      id: "cjr",
      name: "CJR",
      shortDescription: "EJ de Computação",
      category: "Empresas Juniores",
      logo: "/cjr.png",
      tags: ["desenvolvimento_web", "desenvolvimento_backend"],
      about:
        "A CJR é a Empresa Júnior do curso de Ciência da Computação da UnB. Desenvolvemos soluções web e mobile personalizadas para empresas e organizações.",
      mission:
        "Entregar soluções tecnológicas de qualidade enquanto desenvolvemos os melhores profissionais de tecnologia.",
      vision: "Ser referência em desenvolvimento de software no Distrito Federal até 2026.",
      values: "Qualidade, Inovação, Comprometimento e Crescimento Mútuo.",
      services: "Desenvolvimento web, aplicativos mobile, sistemas personalizados, consultoria em TI.",
      social: {
        instagram: "https://www.instagram.com/cjr.unb/",
        website: "https://www.cjr.org.br/",
      },
    },
  ]
  