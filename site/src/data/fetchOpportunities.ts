import ejLogoMap from "./ejLogos"
import labLogoMap from "./labsLogos"

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
  id: string
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
  tags: Array<{
    id: string
    label: string
    categoria: string
    subcategoria: string
  }>
}

export interface OportunidadesCompletoJSON {
  metodo: string
  modelo_embedding: string
  total_oportunidades: number
  total_laboratorios: number
  total_empresas_juniores: number
  laboratorios: LaboratorioRaw[]
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

function resolveEjLogoById(id: string): string | "" {
  return ejLogoMap[id] ?? ""
}

function resolveLabLogoById(id: string): string | "" {
  return labLogoMap[id] ?? ""
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
    logo: resolveLabLogoById(lab.id),
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

  // Extrair tags do array de tags (se existir) ou usar tag padrão
  const tagIds = ej.tags && ej.tags.length > 0 
    ? ej.tags.map(t => t.id)
    : ["empresa_junior"]

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
    logo: resolveEjLogoById(ej.id) || resolveLogoByName(ej.Nome),
    tags: tagIds,
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
    const response = await fetch("/json/oportunidades.json")

    if (!response.ok) {
      console.warn("Não foi possível buscar oportunidades:", response.status)
      return []
    }

    const data = await response.json() as {
      laboratorios?: any[]
      empresas_juniores?: any[]
    }

    
    const opportunities: Opportunity[] = []

    // Processar laboratórios
    try {
      const laboratorios = data.laboratorios || []
      const labOpportunities = laboratorios.map(convertLaboratorioToOpportunity)
      opportunities.push(...labOpportunities)
    } catch (error) {
      console.error("Erro ao processar laboratórios:", error)
    }

    // Processar empresas juniores
    try {
      const empresasJuniores = data.empresas_juniores || []
      const ejOpportunities = empresasJuniores.map(convertEmpresaJuniorToOpportunity)
      opportunities.push(...ejOpportunities)
    } catch (error) {
      console.error("Erro ao processar empresas juniores:", error)
    }

    return opportunities
  } catch (error) {
    console.error("Erro ao buscar oportunidades do JSON unificado:", error)
    return []
  }
}
