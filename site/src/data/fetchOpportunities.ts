import type { Opportunity } from "./opportunities"

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

// Tentativa de resolução de logo baseada no nome, utilizando imagens em public/
function resolveLogoByName(name: string): string | "" {
  const n = name.toLowerCase()
  if (n.includes("orc")) return "/orc.png"
  if (n.includes("eletronjun")) return "/eletronjun.png"
  if (n.includes("zenit")) return "/zenit.png"
  if (n.includes("matriz")) return "/matriz.png"
  if (n.includes("engrena")) return "/engrena.png"
  if (n.includes("cjr")) return "/cjr.png"
  return ""
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
    // Tenta resolver logo por nome (caso seja uma EJ conhecida presente no JSON)
    logo: resolveLogoByName(lab.nome),
    tags: tagIds,
    about: lab.descricao,
    // Contato geralmente é um email, então não adicionamos como website
    // Se houver necessidade de adicionar website, pode ser feito via outro campo
    social: undefined,
  }
}

export async function fetchOpportunitiesFromJSON(): Promise<Opportunity[]> {
  try {
    const response = await fetch("/oportunidade.json")
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json() as OportunidadesJSON
    const laboratorios = data.laboratorios || []
    
    // Converter laboratórios para oportunidades
    const opportunities = laboratorios.map(convertLaboratorioToOpportunity)
    
    return opportunities
  } catch (error) {
    console.error("Erro ao buscar oportunidades do JSON:", error)
    return []
  }
}

