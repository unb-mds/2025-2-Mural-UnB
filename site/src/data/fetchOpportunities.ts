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

export interface LaboratorioRaw {
  id: number
  nome: string
  coordenador: string
  contato: string
  descricao: string
  tags: Array<{
    id: string
    label: string
    categoria: string
    subcategoria: string
  }>
  total_tags?: number
  top_tags_scores?: Array<{
    label: string
    score: number
  }>
}

export interface OportunidadesJSON {
  metodo: string
  modelo_embedding: string
  total_laboratorios: number
  data_geracao: string
  parametros: {
    min_tags: number
    max_tags: number
    threshold_similaridade: number
  }
  laboratorios: LaboratorioRaw[]
}

export interface EmpresaJuniorRaw {
  id: string
  Nome: string
  Cursos: string
  Sobre: string
  Missao: string
  Visao: string
  Valores: string
  Servicos: string
  Site: string
  Instagram: string
}

export interface EmpresasJunioresJSON {
  metadados: {
    data_processamento: string
    total_empresas_unicas: number
    total_empresas_bruto: number
    processamento_pagina: boolean
    pagina_inicial: number
  }
  empresas_juniores: EmpresaJuniorRaw[]
}

// Tentativa de resolução de logo baseada no nome, utilizando imagens em public/
function resolveLogoByName(name: string): string | "" {
  const n = name.toLowerCase()
  if (n.includes("orc") || n.includes("orc'estra") || n.includes("orcestra")) return "/orc.png"
  if (n.includes("eletronjun") || n.includes("eletrojun")) return "/eletronjun.png"
  if (n.includes("zenit")) return "/zenit.png"
  if (n.includes("matriz")) return "/matriz.png"
  if (n.includes("engrena")) return "/engrena.png"
  if (n.includes("cjr")) return "/cjr.png"
  return ""
}

// Normalizar URL do Instagram para formato completo
function normalizeInstagramUrl(instagram: string): string {
  if (!instagram) return ""
  const cleaned = instagram.replace("@", "").trim()
  if (cleaned.startsWith("http")) return cleaned
  return `https://www.instagram.com/${cleaned}/`
}

// Normalizar URL do site para formato completo
function normalizeWebsiteUrl(site: string): string {
  if (!site || site === "N/A") return ""
  const cleaned = site.trim()
  if (cleaned.startsWith("http")) return cleaned
  return `https://${cleaned}`
}

function determineCategory(tags: LaboratorioRaw["tags"]): string {
  // Verificar se é laboratório, equipe competitiva, ou empresa júnior baseado nas tags
  const tagIds = tags.map(t => t.id.toLowerCase())
  
  // Verificar se é equipe competitiva
  if (tagIds.includes("equipe_competicao") || tagIds.some(id => id.includes("equipe"))) {
    return "Equipes Competitivas"
  }
  
  // Verificar se é empresa júnior
  if (tagIds.some(id => id.includes("empresa_junior") || id.includes("ej") || id.includes("empresa junior"))) {
    return "Empresas Juniores"
  }
  
  // Por padrão, se tem laboratorio_pesquisa ou é do tipo laboratório, é um laboratório
  if (tagIds.includes("laboratorio_pesquisa") || tagIds.some(id => id.includes("laboratorio"))) {
    return "Laboratórios"
  }
  
  // Fallback: se não tem nenhuma tag específica, assume que é laboratório
  return "Laboratórios"
}

function convertLaboratorioToOpportunity(lab: LaboratorioRaw): Opportunity {
  const tagIds = lab.tags.map(t => t.id)
  const category = determineCategory(lab.tags)
  
  // Criar shortDescription baseado na descrição (primeiras palavras)
  const shortDescription = lab.descricao.length > 100 
    ? lab.descricao.substring(0, 100) + "..."
    : lab.descricao

  return {
    id: `lab-${lab.id}`,
    name: lab.nome,
    shortDescription: shortDescription,
    category: category,
    logo: resolveLogoByName(lab.nome),
    tags: tagIds,
    about: lab.descricao,
    social: undefined,
  }
}

function convertEmpresaJuniorToOpportunity(ej: EmpresaJuniorRaw): Opportunity {
  // Criar shortDescription baseado no campo Sobre (primeiras palavras)
  const shortDescription = ej.Sobre.length > 100 
    ? ej.Sobre.substring(0, 100) + "..."
    : ej.Sobre

  // Criar tags básicas baseadas na categoria (sempre será Empresa Júnior)
  const tags = ["empresa_junior"]

  // Construir objeto social com Instagram e Site
  const social: { instagram?: string; website?: string } = {}
  if (ej.Instagram && ej.Instagram !== "N/A") {
    social.instagram = normalizeInstagramUrl(ej.Instagram)
  }
  if (ej.Site && ej.Site !== "N/A") {
    social.website = normalizeWebsiteUrl(ej.Site)
  }

  return {
    id: `ej-${ej.id}`,
    name: ej.Nome,
    shortDescription: shortDescription,
    category: "Empresas Juniores",
    logo: resolveLogoByName(ej.Nome),
    tags: tags,
    about: ej.Sobre,
    mission: ej.Missao !== "N/A" ? ej.Missao : undefined,
    vision: ej.Visao !== "N/A" ? ej.Visao : undefined,
    values: ej.Valores !== "N/A" ? ej.Valores : undefined,
    services: ej.Servicos !== "N/A" ? ej.Servicos : undefined,
    social: Object.keys(social).length > 0 ? social : undefined,
  }
}

export async function fetchOpportunitiesFromJSON(): Promise<Opportunity[]> {
  try {
    // Buscar laboratórios e empresas juniores em paralelo
    const [labsResponse, ejsResponse] = await Promise.all([
      fetch("/json/oportunidade.json"),
      fetch("/json/empresas_juniores_consolidadas.json")
    ])

    const opportunities: Opportunity[] = []

    // Processar laboratórios
    if (labsResponse.ok) {
      try {
        const labsData = await labsResponse.json() as OportunidadesJSON
        const laboratorios = labsData.laboratorios || []
        const labOpportunities = laboratorios.map(convertLaboratorioToOpportunity)
        opportunities.push(...labOpportunities)
      } catch (error) {
        console.error("Erro ao processar laboratórios:", error)
      }
    } else {
      console.warn("Não foi possível buscar laboratórios:", labsResponse.status)
    }

    // Processar empresas juniores
    if (ejsResponse.ok) {
      try {
        const ejsData = await ejsResponse.json() as EmpresasJunioresJSON
        const empresasJuniores = ejsData.empresas_juniores || []
        const ejOpportunities = empresasJuniores.map(convertEmpresaJuniorToOpportunity)
        opportunities.push(...ejOpportunities)
      } catch (error) {
        console.error("Erro ao processar empresas juniores:", error)
      }
    } else {
      console.warn("Não foi possível buscar empresas juniores:", ejsResponse.status)
    }

    return opportunities
  } catch (error) {
    console.error("Erro ao buscar oportunidades do JSON:", error)
    return []
  }
}

