import ejLogoMap from "./ejLogos"
import labLogoMap from "./labsLogos"
import { EQUIPES_COMPETICAO_FIXAS } from "./equipesCompeticao"
import { calcularEmbeddingsEquipes } from "./calcularEmbeddingsEquipes"
import { fetchTagsFlat } from "./fetchTags"

export interface Opportunity {
  id: string
  name: string
  campus: string // Campo já existente na sua interface
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
  embedding?: number[] 
}

export interface LaboratorioRaw {
  id: string
  nome: string
  campus: string 
  coordenador: string
  contato: string
  descricao: string
  Site?: string
  Instagram?: string
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
  embedding_agregado?: number[]
}


export interface EmpresaJuniorRaw {
  id: string
  Nome: string
  Campus?: string 
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
  embedding_agregado?: number[]
}

export interface OportunidadesCompletoJSON {
  metodo: string
  modelo_embedding?: string
  total_oportunidades?: number
  total_laboratorios?: number
  total_empresas_juniores?: number
  laboratorios?: LaboratorioRaw[]
  empresas_juniores?: EmpresaJuniorRaw[]
}

// --- Funções Auxiliares de Logo ---
function resolveLogoByName(name: string): string | "" {
  const base = import.meta.env.BASE_URL || '/'
  const resolvePath = (path: string) => base.endsWith('/') ? `${base}${path.slice(1)}` : `${base}${path}`
  
  const n = name.toLowerCase()
  if (n.includes("orc") || n.includes("orc'estra") || n.includes("orcestra")) return resolvePath("/orc.png")
  if (n.includes("eletronjun") || n.includes("eletrojun")) return resolvePath("/eletronjun.png")
  if (n.includes("zenit")) return resolvePath("/zenit.png")
  if (n.includes("matriz")) return resolvePath("/matriz.png")
  if (n.includes("engrena")) return resolvePath("/engrena.png")
  if (n.includes("cjr")) return resolvePath("/cjr.png")
  return ""
}

function resolveEjLogoById(id: string): string | "" {
  return ejLogoMap[id] ?? ""
}

function resolveLabLogoById(id: string): string | "" {
  return labLogoMap[id] ?? ""
}

// --- Normalizadores de URL ---
function normalizeInstagramUrl(instagram: string): string {
  if (!instagram) return ""
  const cleaned = instagram.replace("@", "").trim()
  if (cleaned.startsWith("http")) return cleaned
  return `https://www.instagram.com/${cleaned}/`
}

function normalizeWebsiteUrl(site: string): string {
  if (!site || site === "N/A") return ""
  const cleaned = site.trim()
  if (cleaned.startsWith("http")) return cleaned
  return `https://${cleaned}`
}

// --- Helper Robusto para extrair Embedding ---
function extractEmbedding(item: any): number[] {
  // Tenta o nome correto primeiro
  if (Array.isArray(item.embedding_agregado) && item.embedding_agregado.length > 0) return item.embedding_agregado;
  
  // Fallbacks para outros nomes comuns
  if (Array.isArray(item.embedding) && item.embedding.length > 0) return item.embedding;
  if (Array.isArray(item.Embedding) && item.Embedding.length > 0) return item.Embedding;
  
  return [];
}

function determineCategory(tags: LaboratorioRaw["tags"]): string {
  const tagIds = tags.map(t => t.id.toLowerCase())
  // Não verifica equipes aqui, pois elas são fixas e não vêm do JSON
  if (tagIds.some(id => id.includes("empresa_junior") || id.includes("ej") || id.includes("empresa junior"))) return "Empresas Juniores"
  return "Laboratórios"
}

function convertLaboratorioToOpportunity(lab: LaboratorioRaw): Opportunity {
  const tagIds = lab.tags.map(t => t.id)
  const category = determineCategory(lab.tags)
  
  const shortDescription = lab.descricao.length > 100 
    ? lab.descricao.substring(0, 100) + "..."
    : lab.descricao

  const social: { instagram?: string; website?: string } = {}
  
  if (lab.Instagram && lab.Instagram !== "N/A") {
    social.instagram = normalizeInstagramUrl(lab.Instagram)
  }
  if (lab.Site && lab.Site !== "N/A") {
    social.website = normalizeWebsiteUrl(lab.Site)
  }

  return {
    id: `lab-${lab.id}`,
    name: lab.nome,
    campus: lab.campus || "N/A", 
    shortDescription: shortDescription,
    category: category,
    logo: resolveLabLogoById(lab.id),
    tags: tagIds,
    about: lab.descricao,
    social: Object.keys(social).length > 0 ? social : undefined,
    embedding: extractEmbedding(lab)
  }
}

function convertEmpresaJuniorToOpportunity(ej: EmpresaJuniorRaw): Opportunity {
  const shortDescription = ej.Sobre.length > 100 
    ? ej.Sobre.substring(0, 100) + "..."
    : ej.Sobre

  const tagIds = ej.tags && ej.tags.length > 0 
    ? ej.tags.map(t => t.id)
    : ["empresa_junior"]

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
    campus: ej.Campus || "N/A", 
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
    embedding: extractEmbedding(ej)
  }
}

export async function fetchOpportunitiesFromJSON(): Promise<Opportunity[]> {
  try {
    const basePath = import.meta.env.BASE_URL || '/'
    const url = basePath.endsWith('/') 
      ? `${basePath}json/oportunidades.json` 
      : `${basePath}/json/oportunidades.json`
    console.log('Tentando buscar oportunidades de:', url)
    const response = await fetch(url)

    if (!response.ok) {
      console.warn("Não foi possível buscar oportunidades:", response.status)
      return []
    }

    const data = await response.json() as OportunidadesCompletoJSON
    const opportunities: Opportunity[] = []

    // Processar laboratórios
    if (data.laboratorios) {
      try {
        const labOpportunities = data.laboratorios.map(convertLaboratorioToOpportunity)
        opportunities.push(...labOpportunities)
      } catch (error) {
        console.error("Erro ao processar laboratórios:", error)
      }
    }

    // Processar empresas juniores
    if (data.empresas_juniores) {
      try {
        const ejOpportunities = data.empresas_juniores.map(convertEmpresaJuniorToOpportunity)
        opportunities.push(...ejOpportunities)
      } catch (error) {
        console.error("Erro ao processar empresas juniores:", error)
      }
    }


    try {
      const tags = await fetchTagsFlat()
      const equipesComEmbeddings = calcularEmbeddingsEquipes(tags)
      opportunities.push(...equipesComEmbeddings)
    } catch (error) {
      console.error("Erro ao calcular embeddings das equipes:", error)
      // Fallback: adiciona equipes sem embeddings
      opportunities.push(...EQUIPES_COMPETICAO_FIXAS)
    }

    return opportunities
  } catch (error) {
    console.error("Erro ao buscar oportunidades do JSON unificado:", error)
    return []
  }
}