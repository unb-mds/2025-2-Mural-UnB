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
 * Similaridade = (A · B) / (||A|| * ||B||)
 */
export function cosineSimilarity(vecA: Embedding, vecB: Embedding): number {
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }

  // Lida com divisão por zero caso algum vetor seja nulo
  if (normA === 0 || normB === 0) {
    return 0;
  }

  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}