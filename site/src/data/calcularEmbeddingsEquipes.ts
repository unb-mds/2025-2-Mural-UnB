import type { Tag } from "./tags"
import { calculateMeanVector } from "../utils/vectorMatch"
import { EQUIPES_COMPETICAO_FIXAS } from "./equipesCompeticao"
import type { Opportunity } from "./fetchOpportunities"

export function calcularEmbeddingsEquipes(tags: Tag[]): Opportunity[] {
  const tagEmbeddingMap = new Map<string, number[]>()
  tags.forEach(tag => {
    if (tag.embedding) {
      tagEmbeddingMap.set(tag.id, tag.embedding)
    }
  })

  return EQUIPES_COMPETICAO_FIXAS.map(equipe => {
    if (!equipe.embedding || equipe.embedding.length === 0) {
      const tagEmbeddings: number[][] = []
      
      if (equipe.tags) {
        for (const tagId of equipe.tags) {
          const embedding = tagEmbeddingMap.get(tagId)
          if (embedding) {
            tagEmbeddings.push(embedding)
          }
        }
      }
      
      if (tagEmbeddings.length > 0) {
        return {
          ...equipe,
          embedding: calculateMeanVector(tagEmbeddings)
        }
      }
    }
    
    return equipe
  })
}

