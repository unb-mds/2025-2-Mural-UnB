// src/hooks/useVectorSearch.ts
import { useState, useEffect } from 'react';
// 1. IMPORTA as interfaces de dados que o fetchData vai retornar
import type { ILab, ITagsData, Embedding, ILabsData } from '../utils/types';
// 2. IMPORTA o novo serviço de dados
import { fetchData } from '../utils/dataService';

// Mapeia "tag_id" -> [vetor de embedding]
type TagsLookupMap = Map<string, Embedding>;

interface SearchData {
  allLabs: ILab[];
  allTagsData: ITagsData | null;
  tagsLookup: TagsLookupMap;
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
        setError(null);

        // 3. SUBSTITUI a lógica de fetch antiga
        // Carrega ambos os arquivos em paralelo usando o novo serviço
        const [labsData, tagsData] = await Promise.all([
          fetchData<ILabsData>('labs_com_embedding_agregado.json'),
          fetchData<ITagsData>('tags.json')
        ]);

        // 4. VERIFICA se os dados vieram (fetchData retorna null em erro)
        if (!labsData || !tagsData) {
          throw new Error('Falha ao carregar um ou mais arquivos de dados');
        }

        // 5. PROCESSAMENTO
        // Processa e armazena os laboratórios
        setAllLabs(labsData.laboratorios || []);

        // Processa e armazena os dados brutos das tags (para a UI)
        setAllTagsData(tagsData);

        // Cria o Mapa de Lookup para performance
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
  }, []);

  return { allLabs, allTagsData, tagsLookup, isLoading, error };
}