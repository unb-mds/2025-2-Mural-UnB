import { useEffect, useState } from "react"
// Importa a função matemática criada acima
import { calculateMeanEmbedding } from "../../utils/vectorMatch"

import { type Tag } from "../../data/tags"

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

interface TagsFilterModalProps {
  isOpen: boolean
  onClose: () => void
  tags: Tag[]
  selectedTags: string[]
  onTagToggle: (tagId: string) => void
  onSave?: (selectedTags: string[]) => void
}

export default function TagsFilterModal({ isOpen, onClose, tags, selectedTags, onTagToggle, onSave }: TagsFilterModalProps) {
  const [tagsData, setTagsData] = useState<TagsJSON | null>(null)

  // Carrega o JSON completo de tags
  useEffect(() => {
    if (!isOpen) return
    
    const loadTagsData = async () => {
      try {
        const basePath = import.meta.env.BASE_URL || '/'
        const url = basePath.endsWith('/') 
          ? `${basePath}json/tags.json` 
          : `${basePath}/json/tags.json`
        const res = await fetch(url)
        if (!res.ok) throw new Error(`HTTP error ${res.status}`)
        const data = await res.json() as TagsJSON
        setTagsData(data)
      } catch (error) {
        console.error("Erro ao carregar tags.json:", error)
      }
    }
    
    loadTagsData()
  }, [isOpen])

  // Função auxiliar de segurança: busca o embedding no JSON bruto caso a prop 'tags' venha incompleta
  const findEmbeddingInRawData = (tagId: string): number[] | undefined => {
    if (!tagsData) return undefined;

    for (const categoria of tagsData.categorias || []) {
      if (!categoria.subcategorias) continue;
      for (const sub of categoria.subcategorias) {
        if (!sub.tags) continue;
        const foundTag = sub.tags.find((t: any) => t.id === tagId);
        if (foundTag && Array.isArray(foundTag.embedding)) {
          return foundTag.embedding;
        }
      }
    }
    return undefined;
  }

  const handleSave = () => {
    // 1. Salva a lista de IDs (apenas strings)
    // Isso só acontece agora, ao clicar em "Salvar"
    localStorage.setItem('selectedTags', JSON.stringify(selectedTags))
    
    // 2. Calcula e Salva o Vetor de Preferências (Embeddings)
    try {
      const embeddings = selectedTags.map(tagId => {
        // Tenta pegar da prop tags (mais rápido e ideal)
        const tagFromProp = tags.find(t => t.id === tagId);
        if (tagFromProp?.embedding && Array.isArray(tagFromProp.embedding)) {
          return tagFromProp.embedding;
        }
        // Fallback: busca no JSON importado
        return findEmbeddingInRawData(tagId);
      }).filter((emb): emb is number[] => Array.isArray(emb) && emb.length > 0);

      if (embeddings.length > 0) {
        const meanVector = calculateMeanEmbedding(embeddings)
        if (meanVector) {
          localStorage.setItem("userMeanEmbedding", JSON.stringify(meanVector))
          // console.log("Vetor de preferências atualizado.")
        }
      } else {
        // Se o usuário limpou a seleção, removemos o vetor antigo
        localStorage.removeItem("userMeanEmbedding")
      }
    } catch (error) {
      console.error("Erro ao processar embeddings:", error)
    }

    // 3. Notifica o componente pai e fecha
    if (onSave) {
      onSave(selectedTags)
    }
    
    onClose()
  }

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden"
    } else {
      document.body.style.overflow = "unset"
    }
    return () => {
      document.body.style.overflow = "unset"
    }
  }, [isOpen])

  if (!isOpen) return null

  // Lógica para organizar as tags por subcategoria para exibição
  const tagsBySubcategory: { [key: string]: Tag[] } = {}
  
  if (tagsData) {
    tagsData.categorias.forEach((category) => {
      if (category.subcategorias) {
        category.subcategorias.forEach((sub) => {
          const subName = sub.nome_subcategoria?.trim();
          
          // Ignora subcategorias sem nome (serão tratadas como "Outros" depois)
          if (!subName || !sub.tags) return;
          
          // Filtra apenas as tags que existem na prop 'tags' passada para o modal
          const matchingTags = sub.tags.filter((jsonTag) => 
            tags.some(t => t.id === jsonTag.id)
          );
          
          if (matchingTags.length > 0) {
            // Mapeia para o formato Tag
            const tagsDestaSubcategoria = matchingTags.map((t) => ({ 
              id: t.id, 
              label: t.label, 
              embedding: t.embedding 
            }));
            
            // Se a subcategoria já existe, adiciona as tags a ela
            if (tagsBySubcategory[subName]) {
              tagsBySubcategory[subName].push(...tagsDestaSubcategoria);
            } else {
              tagsBySubcategory[subName] = tagsDestaSubcategoria;
            }
          }
        });
      }
    });
  }

  // Adiciona tags que não foram encontradas nas subcategorias (Outros)
  const categorizedTagIds = new Set(Object.values(tagsBySubcategory).flat().map((t) => t.id))
  const uncategorizedTags = tags.filter((tag) => !categorizedTagIds.has(tag.id))
  
  if (uncategorizedTags.length > 0) {
    tagsBySubcategory["Outros"] = uncategorizedTags
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Filtrar por Tags</h2>
        </div>

        <div className="modal-body">
          {!tagsData ? (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
              Carregando tags...
            </div>
          ) : Object.keys(tagsBySubcategory).length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
              Nenhuma tag encontrada
            </div>
          ) : (
            Object.entries(tagsBySubcategory).map(([subcategory, subcategoryTags]) => (
              <div key={subcategory} className="tag-category">
                <h3>{subcategory}</h3>
                <div className="tags-list">
                  {subcategoryTags.map((tag) => {
                    const isSelected = selectedTags.includes(tag.id)
                    return (
                      <button
                        key={tag.id}
                        onClick={() => onTagToggle(tag.id)}
                        className={`tag-button ${isSelected ? "selected" : ""}`}
                      >
                        {tag.label}
                        {isSelected && <span className="tag-check">✓</span>}
                      </button>
                    )
                  })}
                </div>
              </div>
            ))
          )}
        </div>

        <div className="modal-footer">
          <button
            onClick={() => {
              selectedTags.forEach(onTagToggle)
            }}
            className="modal-clear-button"
            disabled={selectedTags.length === 0}
          >
            Limpar Seleção ({selectedTags.length})
          </button>
          <button className="modal-save" onClick={handleSave}>
            Salvar
          </button>
        </div>
      </div>
    </div>
  )
}