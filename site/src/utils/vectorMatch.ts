import type { Embedding } from 'utils/types';

/**
 * Calcula a média de múltiplos vetores de embedding.
 */
export function calculateMeanEmbedding(embeddings: Embedding[]): Embedding | null {
  if (!embeddings || embeddings.length === 0) {
    return null;
  }

  const dimension = embeddings[0].length;
  
  const sumVector: Embedding = new Array(dimension).fill(0);

  // Soma todos os vetores
  for (const vec of embeddings) {
    if (vec.length !== dimension) {
      console.warn("Inconsistência na dimensão dos embeddings:", vec);
      continue;
    }
    for (let i = 0; i < dimension; i++) {
      sumVector[i] += vec[i];
    }
  }

  // Divide pela quantidade de vetores para obter a média
  const meanVector = sumVector.map(val => val / embeddings.length);
  return meanVector;
}


/**
 * Calcula a similaridade de cosseno entre dois vetores.
 * Retorna um valor entre -1 (opostos) e 1 (identicos).
 */
export function cosineSimilarity(vecA: Embedding, vecB: Embedding): number {
  // Verificações de segurança
  if (!vecA || !vecB || vecA.length !== vecB.length) return 0;

  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }

  // Evita divisão por zero
  if (normA === 0 || normB === 0) return 0;

  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * Calcula o score de match para uma lista de itens baseados em um vetor alvo.
 * @param items Lista de objetos que contêm um embedding
 * @param targetVector O vetor do usuário
 * @returns Lista ordenada por similaridade (maior para menor) com score anexado
 */
export function rankBySimilarity<T extends { embedding?: Embedding }>(
  items: T[], 
  targetVector: Embedding
): Array<T & { score: number }> {
  if (!targetVector) return items.map(item => ({ ...item, score: 0 }));

  const ranked = items.map(item => {
    const score = item.embedding 
      ? cosineSimilarity(targetVector, item.embedding) 
      : -1; // Penaliza itens sem embedding
    return { ...item, score };
  });

  // Ordena decrescente (Melhor match primeiro)
  return ranked.sort((a, b) => b.score - a.score);
}

export function calculateMeanVector(vectors: number[][]): number[] {
  if (vectors.length === 0) return [];

  const dimension = vectors[0].length;
  const mean = new Array(dimension).fill(0);

  // Soma todos os vetores
  for (const vector of vectors) {
    for (let i = 0; i < dimension; i++) {
      mean[i] += vector[i];
    }
  }

  // Divide pela quantidade (Média)
  // Se vectors.length for 1, ele divide por 1, mantendo o valor original.
  for (let i = 0; i < dimension; i++) {
    mean[i] /= vectors.length;
  }

  return mean;
}