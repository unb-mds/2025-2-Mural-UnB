export interface Tag {
    id: string
    label: string
  }
  
  export interface TagCategories {
    [category: string]: Tag[]
  }
  
  export const allTags: TagCategories = {
    "Engenharia de Software": [
      { id: "desenvolvimento_web", label: "Desenvolvimento Web" },
      { id: "desenvolvimento_backend", label: "Desenvolvimento Backend" },
      { id: "desenvolvimento_frontend", label: "Desenvolvimento Frontend" },
      { id: "desenvolvimento_mobile", label: "Desenvolvimento Mobile" },
      { id: "desenvolvimento_jogos", label: "Desenvolvimento de Jogos" },
      { id: "inteligencia_artificial", label: "Inteligência Artificial" },
      { id: "machine_learning", label: "Machine Learning" },
      { id: "deep_learning", label: "Deep Learning" },
      { id: "visao_computacional", label: "Visão Computacional" },
      { id: "pln", label: "Processamento de Linguagem Natural" },
      { id: "ciencia_dados", label: "Ciência de Dados" },
      { id: "analise_dados", label: "Análise de Dados" },
      { id: "big_data", label: "Big Data" },
      { id: "banco_dados_sql", label: "Banco de Dados SQL" },
      { id: "banco_dados_nosql", label: "Banco de Dados NoSQL" },
      { id: "arquitetura_software", label: "Arquitetura de Software" },
      { id: "microsservicos", label: "Microsserviços" },
      { id: "cloud_computing", label: "Computação em Nuvem" },
      { id: "devops", label: "DevOps" },
      { id: "seguranca_informacao", label: "Segurança da Informação" },
      { id: "engenharia_dados", label: "Engenharia de Dados" },
      { id: "qa_testes", label: "Qualidade de Software (QA)" },
      { id: "sistemas_operacionais", label: "Sistemas Operacionais" },
      { id: "redes_computadores", label: "Redes de Computadores" },
      { id: "realidade_virtual_aumentada", label: "Realidade Virtual/Aumentada" },
      { id: "blockchain", label: "Blockchain" },
    ],
    "Engenharia Eletrônica e de Energia": [
      { id: "sistemas_embarcados", label: "Sistemas Embarcados" },
      { id: "microcontroladores_processadores", label: "Microcontroladores" },
      { id: "circuitos_digitais_analogicos", label: "Circuitos Digitais e Analógicos" },
      { id: "eletronica_potencia", label: "Eletrônica de Potência" },
      { id: "processamento_sinais_dsp", label: "Processamento Digital de Sinais" },
      { id: "sistemas_controle", label: "Sistemas de Controle" },
      { id: "robotica", label: "Robótica" },
      { id: "iot", label: "Internet das Coisas (IoT)" },
      { id: "hdl_fpga_asic", label: "VHDL/Verilog e FPGAs" },
      { id: "telecomunicacoes", label: "Telecomunicações" },
      { id: "energias_renovaveis", label: "Energias Renováveis" },
      { id: "sistemas_eletricos_potencia", label: "Sistemas Elétricos de Potência" },
      { id: "smart_grids", label: "Redes Elétricas Inteligentes" },
      { id: "armazenamento_energia", label: "Armazenamento de Energia" },
    ],
    "Engenharia Aeroespacial": [
      { id: "aerodinamica", label: "Aerodinâmica" },
      { id: "dinamica_voo", label: "Dinâmica de Voo" },
      { id: "sistemas_propulsao", label: "Sistemas de Propulsão" },
      { id: "estruturas_aeroespaciais", label: "Estruturas Aeroespaciais" },
      { id: "materiais_compositos", label: "Materiais Compósitos" },
      { id: "mecanica_orbital", label: "Mecânica Orbital" },
      { id: "gnc", label: "Guiagem, Navegação e Controle" },
      { id: "satelites_cubesats", label: "Satélites e CubeSats" },
      { id: "foguetes", label: "Foguetes" },
      { id: "vants_drones", label: "VANTs/Drones" },
      { id: "modelagem_simulacao_aero", label: "Modelagem e Simulação" },
      { id: "avionica", label: "Aviônica" },
    ],
    "Engenharia Automotiva": [
      { id: "dinamica_veicular", label: "Dinâmica Veicular" },
      { id: "sistemas_automotivos", label: "Sistemas Automotivos" },
      { id: "motores_combustao", label: "Motores a Combustão" },
      { id: "mobilidade_eletrica", label: "Mobilidade Elétrica" },
      { id: "veiculos_autonomos", label: "Veículos Autônomos" },
      { id: "eletronica_automotiva_embarcada", label: "Eletrônica Embarcada" },
      { id: "design_automotivo_cad", label: "Design Automotivo e CAD" },
      { id: "powertrain", label: "Powertrain" },
    ],
    "Linguagens de Programação": [
      { id: "python", label: "Python" },
      { id: "c_cpp", label: "C/C++" },
      { id: "java", label: "Java" },
      { id: "javascript_ts", label: "JavaScript/TypeScript" },
      { id: "matlab", label: "MATLAB" },
      { id: "sql", label: "SQL" },
      { id: "rust", label: "Rust" },
      { id: "go", label: "Go" },
      { id: "kotlin", label: "Kotlin" },
    ],
    "Frameworks e Bibliotecas": [
      { id: "react", label: "React" },
      { id: "angular", label: "Angular" },
      { id: "vuejs", label: "Vue.js" },
      { id: "nodejs", label: "Node.js" },
      { id: "django", label: "Django" },
      { id: "flask", label: "Flask" },
      { id: "spring_boot", label: "Spring Boot" },
      { id: "tensorflow", label: "TensorFlow" },
      { id: "pytorch", label: "PyTorch" },
      { id: "scikit_learn", label: "Scikit-learn" },
      { id: "pandas", label: "Pandas" },
      { id: "opencv", label: "OpenCV" },
      { id: "ros", label: "ROS" },
    ],
    "Soft Skills": [
      { id: "lideranca", label: "Liderança" },
      { id: "trabalho_equipe", label: "Trabalho em Equipe" },
      { id: "comunicacao", label: "Comunicação" },
      { id: "oratória_apresentacao", label: "Oratória e Apresentação" },
      { id: "resolucao_problemas", label: "Resolução de Problemas" },
      { id: "pensamento_critico", label: "Pensamento Crítico" },
      { id: "criatividade_inovacao", label: "Criatividade e Inovação" },
      { id: "proatividade", label: "Proatividade" },
      { id: "gestao_tempo", label: "Gestão de Tempo" },
      { id: "adaptabilidade", label: "Adaptabilidade" },
      { id: "negociacao", label: "Negociação" },
      { id: "mentoria", label: "Mentoria" },
    ],
  }
  
  export const getAllTagsFlat = (): Tag[] => {
    return Object.values(allTags).flat()
  }
  
  export const getRandomTags = (count = 2): Tag[] => {
    const flatTags = getAllTagsFlat()
    const shuffled = [...flatTags].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, count)
  }
  
  export const tags = getAllTagsFlat()
  