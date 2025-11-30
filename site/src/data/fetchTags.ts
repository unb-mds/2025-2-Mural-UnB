import type { Tag } from "./tags"

interface TagsJSON {
  categorias: Array<{
    nome_categoria: string
    descricao: string
    subcategorias: Array<{
      nome_subcategoria: string
      tags: Array<{
        id: string
        label: string
        description?: string
        embedding?: number[]
      }>
    }>
  }>
}

export async function fetchTagsFlat(): Promise<Tag[]> {
  try {
    const basePath = import.meta.env.BASE_URL || '/'
    const url = `${basePath}json/tags.json`.replace(/\/+/g, '/')
    const res = await fetch(url)
    if (!res.ok) throw new Error(`HTTP error ${res.status}`)
    const data = (await res.json()) as TagsJSON
    const flat: Tag[] = []
    
    for (const cat of data.categorias || []) {
      for (const sub of cat.subcategorias || []) {
        for (const tag of sub.tags || []) {
          // CORREÇÃO: Agora incluímos o embedding e description no objeto final
          flat.push({ 
            id: tag.id, 
            label: tag.label,
            description: tag.description, // Útil ter a descrição também
            embedding: tag.embedding      // <--- O CAMPO CRUCIAL QUE FALTAVA
          } as Tag)
        }
      }
    }
    
    // Remove duplicadas por id
    const seen = new Set<string>()
    const unique: Tag[] = []
    for (const t of flat) {
      if (!seen.has(t.id)) {
        seen.add(t.id)
        unique.push(t)
      }
    }
    return unique
  } catch (e) {
    console.error("Erro ao carregar tags.json:", e)
    return []
  }
}