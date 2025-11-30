import type { Opportunity } from "./fetchOpportunities"

// Helper para resolver caminhos de imagem com base path do Vite
function resolveImagePath(path: string): string {
  const base = import.meta.env.BASE_URL || '/'
  return base.endsWith('/') ? `${base}${path.slice(1)}` : `${base}${path}`
}

export const EQUIPES_COMPETICAO_FIXAS: Opportunity[] = [
  {
    id: "equipe-300001",
    name: "DROID",
    campus: "Darcy",
    shortDescription: "A DROID – Divisão de Robótica Inteligente – é a Equipe de Competição de Robôs da UnB. Compete desde 2009 em torneios nacionais e internacionais de robótica autônoma.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300001.jpg"),
    tags: ["equipe_competicao", "robotica", "inteligencia_artificial", "visao_computacional", "trabalho_equipe"],
    about: "A DROID – Divisão de Robótica Inteligente – é a Equipe de Competição de Robôs da UnB. Compete desde o segundo semestre de 2009 em torneios nacionais e internacionais de Desafio de Robô. A Equipe conta com integrantes das diversas áreas da engenharia. A DROID participa de competições de robótica autônoma que simulam problemas reais e visam o desenvolvimento das tecnologias atuais. O trabalho da equipe consiste em construir robôs, desde sua parte mecânica até a elétrica, e programá-los para resolver o desafio proposto nas competições.\n\nA IEEE-SEK, a IEEE-Open, a RoboCup Festo Logistics da Latin America Robotics Competition (LARC), a Firefighting, a Balancer Race da Robogames, e a RoboCup Work da RoboCup Geman Open são exemplos de categorias que a DROID participa. Também atuam na Semana de Ciência e Tecnologia e outros eventos relacionados. Os robôs são autônomos, ou seja, ninguém os controla diretamente na hora da competição, eles são programados e no desafio apenas executam o que está na sua programação.",
    social: {
      website: "https://www.facebook.com/droidunb"
    },
    embedding: [] 
  },
  {
    id: "equipe-300002",
    name: "Draco Volans - Aerodesign SAE",
    campus: "Darcy",
    shortDescription: "Equipe fundada em 2003 para representar a UnB na Competição SAE Brasil de Aerodesign. Pioneira do Aerodesign na UnB e na região Centro-Oeste.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300002.png"),
    tags: ["equipe_competicao", "engenharia_aeroespacial", "aerodinamica", "estruturas_aeroespaciais", "drones"],
    about: "A equipe Draco Volans foi fundada em 2003 com o objetivo de representar a Universidade de Brasília na Competição SAE Brasil de Aerodesign. A equipe foi a primeira da região Centro-Oeste a participar desta modalidade de evento.\n\nParticipou pela primeira vez da Competição SAE Brasil Aerodesign em setembro de 2004, obtendo a 12ª colocação, que lhe rendeu o título de melhor universidade estreante. Já em 2005, a equipe recebeu o troféu de 5º lugar dentre os 61 participantes. A equipe Draco Volans é pioneira do Aerodesign na Universidade de Brasília e na região Centro-Oeste.\n\nUnidos com o propósito de ter contato com a engenharia aplicada e criada exclusivamente por iniciativa dos alunos, a equipe projeta, constrói e faz voar aeronaves rádio controladas.",
    social: {
      website: "https://www.facebook.com/dracovolans.unb"
    },
    embedding: []
  },
  {
    id: "equipe-300003",
    name: "Piratas do Cerrado - Baja SAE",
    campus: "Darcy",
    shortDescription: "Equipe fundada em 1997 por estudantes de Engenharia para participar de competições Baja SAE. Participa anualmente de competições regionais e nacionais.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300003.jpg"),
    tags: ["equipe_competicao", "engenharia_automotiva", "materiais_compostos", "mecanica_solidos", "trabalho_equipe"],
    about: "A equipe \"Piratas do Cerrado\" foi fundada em 1997 por estudantes de Engenharia da Universidade de Brasília com o objetivo de participar de competições Baja SAE de veículos off-road. A equipe participou de seu primeiro evento um ano após sua criação.\n\nAtualmente, a equipe conta com membros de diversos cursos de graduação e está dividida em 6 áreas de projeto (Powertrain, Freio, Suspensão, Design e Ergonomia, Cálculo Estrutural e Eletrônica) e 4 áreas organizacionais (Gestão, Marketing, Logística e Financeiro).\n\nA competição Baja SAE tem como objetivo estimular os participantes a desenvolverem habilidades fundamentais para o mercado de trabalho, como liderança e trabalho em equipe. Anualmente, a equipe \"Piratas do Cerrado\" participa de duas competições: a Regional Sudeste e a Nacional (que envolve mais de 70 equipes do Brasil). As 3 melhores equipes são convidadas para uma competição internacional nos Estados Unidos.\n\nA subárea de Eletrônica da equipe \"Piratas do Cerrado\" é responsável pelo desenvolvimento de um sistema eletrônico embarcado para monitorar o desempenho do protótipo. Além disso, auxilia na realização de testes, seleção e implementação de sensores e métodos de armazenamento de dados. Os membros aprendem sobre transmissão de dados, microcontroladores, processamento de sinais, seleção de sensores e processos de fabricação.",
    social: {
      website: "https://www.facebook.com/PiratasdoCerrado",
      instagram: "https://www.instagram.com/piratas_do_cerrado/"
    },
    embedding: []
  },
  {
    id: "equipe-300004",
    name: "UnBall - Futebol de Robôs",
    campus: "Darcy",
    shortDescription: "Equipe fundada em 2009 que participa de competições nacionais e internacionais de futebol de robôs usando robôs autônomos.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300004.jpg"),
    tags: ["equipe_competicao", "robotica", "inteligencia_artificial", "visao_computacional", "futebol_robos"],
    about: "A UnBall - Futebol de Robôs foi fundada em 2009. Seu objetivo é participar de competições nacionais e internacionais de robótica, utilizando robôs autônomos para jogar partidas de futebol.\n\nAtualmente, a UnBall participa da LARC/CBR (Latin American Robotics Competition/Competição Brasileira de Robótica) e da IronCup. Competem na categoria IEEE Very Small Size Soccer.\n\nA equipe projeta e constrói seus próprios robôs, enfrentando desafios em mecânica, eletrônica, visão computacional e desenvolvimento de inteligência artificial para os robôs. O projeto é totalmente composto por estudantes voluntários da Universidade de Brasília (UnB). Os estudantes estão envolvidos em todos os aspectos, desde o trabalho técnico até a gestão e seleção da equipe. A UnBall visa complementar a formação acadêmica de seus membros através da aplicação prática da robótica, promovendo troca de experiências em um ambiente de inovação e aprendizado.\n\nNa categoria IEEE Very Small Soccer, cada equipe é composta por 3 robôs autônomos. Os robôs devem ser cúbicos com dimensões máximas de 75 mm por lado. A localização dos robôs no campo é feita via câmera. Cada equipe deve desenvolver seu próprio sistema de visão computacional. Os robôs se comunicam sem fio com um computador central. A UnBall desenvolve tanto o projeto da placa eletrônica quanto a modelagem mecânica para seus robôs. Seus robôs são impressos em 3D.",
    social: {},
    embedding: []
  },
  {
    id: "equipe-300005",
    name: "UnBeatables - Futebol de Robôs Humanoides",
    campus: "Darcy",
    shortDescription: "Equipe de futebol de robôs humanoides da UnB fundada em 2014. Representa a UnB em campeonatos regionais e mundiais, tendo conquistado vários títulos.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300005.jpg"),
    tags: ["equipe_competicao", "robotica", "inteligencia_artificial", "visao_computacional", "humanoides"],
    about: "A UnBeatables é uma equipe de competição de futebol de robôs humanoides da Universidade de Brasília (UnB), fundada em 2014. Representa a UnB em campeonatos regionais e mundiais, tendo conquistado vários títulos.\n\nParticipa da RoboCup Standard Platform League, utilizando robôs humanoides NAO. Os robôs são projetados para serem autônomos, tomando decisões sem interferência externa. O trabalho da equipe foca em visão computacional, comportamento, comunicação e locomoção.\n\nAlém de desenvolver habilidades acadêmicas, a UnBeatables busca impactar e beneficiar a comunidade local. Seus projetos de extensão introduzem estudantes do ensino básico à tecnologia de robótica, promovendo conhecimento e incentivando futuras carreiras na área.",
    social: {
      website: "https://www.facebook.com/unbeatablesbr",
      instagram: "https://www.instagram.com/unbeatablesbr/"
    },
    embedding: []
  },
  {
    id: "equipe-300006",
    name: "Apuama Racing - Fórmula SAE Combustão",
    campus: "Darcy",
    shortDescription: "Equipe de Fórmula SAE Combustão da UnB fundada em 2004. Desenvolve protótipos de carros de corrida estilo open wheel para competições SAE.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300006.jpg"),
    tags: ["equipe_competicao", "engenharia_automotiva", "aerodinamica", "powertrain", "gestao_projetos"],
    about: "A Apuama Racing é a equipe de Fórmula SAE Combustão da Universidade de Brasília fundada em 2004.\n\nA competição, que é realizada em diversos países, é promovida pela Society of Automotive Engineers (SAE), entidade sem fins lucrativos sediada nos EUA. Para competir, cada equipe deve desenvolver um protótipo de carro de corrida no estilo open wheel (semelhante a um Fórmula 1), nas categorias combustão ou elétrico. As equipes são avaliadas rigorosamente, desde os elementos mais simples de projeto até o estudo de mercado para a produção em larga escala do seu protótipo.\n\nA equipe conta com membros de diversos cursos da universidade, distribuídos nas áreas de projeto e de gestão da equipe.",
    social: {
      website: "https://www.facebook.com/ApuamaRacing"
    },
    embedding: []
  },
  {
    id: "equipe-300007",
    name: "Titans",
    campus: "FGA",
    shortDescription: "Equipe de robótica móvel e inteligência artificial da FGA que constrói robôs para competições de combate, seguidores de linha, autônomos e desafios de IA e eletrônica.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300007.jpg"),
    tags: ["equipe_competicao", "robotica", "inteligencia_artificial", "eletronica", "trabalho_equipe"],
    about: "A Titans é a equipe de robótica móvel e inteligência artificial da FGA. Eles constroem robôs para competições de combate, robôs seguidores de linha, robôs autônomos e desafios de IA e eletrônica.\n\nA Titans integra estudantes de engenharia eletrônica, mecatrônica, software e mecânica, e é conhecida por sua forte comunidade interna e participação em eventos de robótica no Brasil.",
    social: {},
    embedding: []
  },
  {
    id: "equipe-300008",
    name: "UnBaja",
    campus: "FGA",
    shortDescription: "Equipe que representa a UnB na competição Baja SAE, desenvolvendo um carro off-road robusto para terrenos extremos.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300008.jpg"),
    tags: ["equipe_competicao", "engenharia_automotiva", "mecanica_solidos", "sistemas_controle", "trabalho_equipe"],
    about: "A UnBaja é a equipe que representa a UnB na competição Baja SAE, desenvolvendo um carro off-road robusto para terrenos extremos.\n\nOs estudantes projetam o sistema de suspensão, direção, transmissão, freios, chassi e ergonomia, além de realizar testes de impacto e performance.\n\nA equipe tem forte cultura de engenharia aplicada e participa todos os anos da competição nacional, frequentemente com bom desempenho.",
    social: {},
    embedding: []
  },
  {
    id: "equipe-300009",
    name: "EDRA",
    campus: "FGA",
    shortDescription: "Equipe focada em drones, sistemas aéreos autônomos e veículos aéreos não tripulados (VANTs). Referência em inteligência embarcada na UnB.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300009.jpg"),
    tags: ["equipe_competicao", "drones", "sistemas_autonomos", "engenharia_aeroespacial", "visao_computacional"],
    about: "A EDRA é uma equipe focada em drones, sistemas aéreos autônomos e veículos aéreos não tripulados (VANTs).\n\nA equipe participa de competições de drones autônomos, realizando tarefas como mapeamento, navegação, busca de alvos, pouso automático e processamento de imagens.\n\nA EDRA combina conhecimentos de engenharia aeroespacial, computação, eletrônica e controle, sendo uma equipe de referência em inteligência embarcada na UnB.",
    social: {},
    embedding: []
  },
  {
    id: "equipe-300010",
    name: "Mamutes do Cerrado",
    campus: "FGA",
    shortDescription: "Equipe de AeroDesign da FGA que projeta e constrói aeronaves rádio controladas com alta eficiência estrutural e aerodinâmica para a competição SAE AeroDesign.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300010.jpg"),
    tags: ["equipe_competicao", "engenharia_aeroespacial", "aerodinamica", "estruturas_aeroespaciais", "propulsao"],
    about: "Os Mamutes do Cerrado são a equipe de AeroDesign da FGA. Eles projetam e constroem aeronaves rádio controladas com alta eficiência estrutural e aerodinâmica para a competição SAE AeroDesign.\n\nO trabalho da equipe inclui dimensionamento de asas, fuselagens, sistemas de propulsão, análise de cargas e otimizações para transportar o máximo de peso possível.\n\nA equipe tem tradição e já participou de várias edições da SAE Brasil.",
    social: {},
    embedding: []
  },
  {
    id: "equipe-300011",
    name: "Capital Rocket Team (CRT)",
    campus: "FGA",
    shortDescription: "Equipe de foguetes da UnB, formada principalmente por estudantes da FGA. Projeta, desenvolve e lança foguetes experimentais de alta potência.",
    category: "Equipe de Competição",
    logo: resolveImagePath("/images/eqc/300011.jpg"),
    tags: ["equipe_competicao", "foguetes", "engenharia_aeroespacial", "propulsao", "estruturas_aeroespaciais"],
    about: "A Capital Rocket Team é a equipe de foguetes da UnB, formada principalmente por estudantes da FGA. O grupo projeta, desenvolve e lança foguetes experimentais, competindo em eventos nacionais e internacionais de foguetes de alta potência.\n\nEles trabalham com aerodinâmica, propulsão, eletrônica embarcada, estrutura, recuperação e simulações. O CRT já conquistou prêmios importantes e é uma das equipes de foguetes mais reconhecidas do Brasil.",
    social: {},
    embedding: []
  }
]
    