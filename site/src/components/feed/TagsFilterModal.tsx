import { useEffect } from "react"
// Certifique-se que este caminho aponta para onde você define seus dados estáticos ou tipos
import { allTags as tagsFromData } from "../../data/tags"
// Importa a função matemática criada acima
import { calculateMeanEmbedding } from "../../utils/vectorMatch"

import { type Tag } from "../../data/tags"

interface TagsFilterModalProps {
  isOpen: boolean
  onClose: () => void
  tags: Tag[]
  selectedTags: string[]
  onTagToggle: (tagId: string) => void
  onSave?: (selectedTags: string[]) => void
}

export default function TagsFilterModal({ isOpen, onClose, tags, selectedTags, onTagToggle, onSave }: TagsFilterModalProps) {
  
  // Função auxiliar de segurança: busca o embedding no JSON bruto caso a prop 'tags' venha incompleta
  const findEmbeddingInRawData = (tagId: string): number[] | undefined => {
    const raw = tagsFromData as any;
    // Tenta acessar categorias direto ou dentro de uma propriedade 'categorias'
    const categorias = Array.isArray(raw) ? raw : (raw.categorias || []);

    for (const categoria of categorias) {
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

  // Lógica para organizar as tags por categoria para exibição
  const tagsByCategory: { [key: string]: Tag[] } = {}
  const raw = tagsFromData as any;
  const categoriasArray = Array.isArray(raw) ? raw : (raw.categorias || []);

  categoriasArray.forEach((category: any) => {
    const catName = category.nome_categoria || "Outros";
    const tagsDestaCategoria: Tag[] = [];
    
    if (category.subcategorias) {
      category.subcategorias.forEach((sub: any) => {
        if (sub.tags) {
          // Filtra apenas as tags que existem na prop 'tags' passada para o modal
          const matchingTags = sub.tags.filter((jsonTag: any) => 
            tags.some(t => t.id === jsonTag.id)
          );
          
          // Mapeia para o formato Tag
          tagsDestaCategoria.push(...matchingTags.map((t: any) => ({ 
            id: t.id, 
            label: t.label, 
            embedding: t.embedding 
          })));
        }
      });
    }

    if (tagsDestaCategoria.length > 0) {
      tagsByCategory[catName] = tagsDestaCategoria;
    }
  });

  // Adiciona tags que não foram encontradas nas categorias (Outros)
  const categorizedTagIds = new Set(Object.values(tagsByCategory).flat().map((t) => t.id))
  const uncategorizedTags = tags.filter((tag) => !categorizedTagIds.has(tag.id))
  
  if (uncategorizedTags.length > 0) {
    tagsByCategory["Outros"] = uncategorizedTags
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Filtrar por Tags</h2>
        </div>

        <div className="modal-body">
          {Object.entries(tagsByCategory).map(([category, categoryTags]) => (
            <div key={category} className="tag-category">
              <h3>{category}</h3>
              <div className="tags-list">
                {categoryTags.map((tag) => {
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
          ))}
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