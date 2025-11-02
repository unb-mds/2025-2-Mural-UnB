// src/hooks/useVectorSearch.ts
import { useState, useEffect } from 'react';
import type { ILab, ITagsData, Embedding, ITag } from '../utils/types';

// O mapa de lookup é a estrutura de dados mais importante para performance.
// Mapeia "tag_id" -> [vetor de embedding]
type TagsLookupMap = Map<string, Embedding>;

interface SearchData {
  allLabs: ILab[];
  allTagsData: ITagsData | null; // Para a UI do seletor
  tagsLookup: TagsLookupMap; // Para a busca
  isLoading: boolean;
  error: Error | null;
}

export function useVectorSearch(): SearchData {
  const [allLabs, setAllLabs] = useState<ILab[]>([]);
  const [allTagsData, setAllTagsData] = useState<ITagsData | null>(null);
  const [tagsLookup, setTagsLookup] = useState<TagsLookupMap>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setIsLoading(true);
        
        // 1. Carrega ambos os arquivos em paralelo
        const [labsResponse, tagsResponse] = await Promise.all([
          fetch('/labs_com_embedding_agregado.json'),
          fetch('/tags.json')
        ]);

        if (!labsResponse.ok || !tagsResponse.ok) {
          throw new Error('Falha ao carregar arquivos JSON');
        }

        const labsData = await labsResponse.json();
        const tagsData: ITagsData = await tagsResponse.json();

        // 2. Processa e armazena os laboratórios
        setAllLabs(labsData.laboratorios || []);
        
        // 3. Processa e armazena os dados brutos das tags (para a UI)
        setAllTagsData(tagsData);

        // 4. Cria o Mapa de Lookup para performance
        const lookup = new Map<string, Embedding>();
        tagsData.categorias.forEach(categoria => {
          categoria.subcategorias.forEach(sub => {
            sub.tags.forEach(tag => {
              if (tag.id && tag.embedding) {
                lookup.set(tag.id, tag.embedding);
              }
            });
          });
        });
        setTagsLookup(lookup);

      } catch (err) {
        setError(err as Error);
      } finally {
        setIsLoading(false);
      }
    }

    loadData();
  }, []); // Executa apenas uma vez

  return { allLabs, allTagsData, tagsLookup, isLoading, error };
}