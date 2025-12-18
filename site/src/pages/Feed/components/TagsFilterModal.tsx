import { useEffect, useState } from "react"
// Importa a função matemática criada acima
import { calculateMeanEmbedding } from "../../../utils/vectorMatch"

import { type Tag } from "../../../data/tags"

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
    <div 
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-[1000] p-4" 
      onClick={onClose}
    >
      <div 
        className="bg-white rounded-xl max-w-[600px] w-full max-h-[80vh] flex flex-col shadow-[0_20px_25px_-5px_rgba(0,0,0,0.1),0_10px_10px_-5px_rgba(0,0,0,0.04)]" 
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-[#e5e5e5]">
          <h2 className="text-2xl font-bold text-[#1a1a1a] m-0">Filtrar por Tags</h2>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto flex-1">
          {!tagsData ? (
            <div className="text-center p-8">
              Carregando tags...
            </div>
          ) : Object.keys(tagsBySubcategory).length === 0 ? (
            <div className="text-center p-8">
              Nenhuma tag encontrada
            </div>
          ) : (
            Object.entries(tagsBySubcategory).map(([subcategory, subcategoryTags]) => (
              <div key={subcategory} className="mb-8 last:mb-0">
                <h3 className="text-base font-semibold text-[#1a1a1a] mb-4 pb-2 border-b-2 border-[#e5e5e5]">
                  {subcategory}
                </h3>
                <div className="flex flex-wrap gap-2">
                  {subcategoryTags.map((tag) => {
                    const isSelected = selectedTags.includes(tag.id)
                    return (
                      <button
                        key={tag.id}
                        onClick={() => onTagToggle(tag.id)}
                        className={`py-2 px-4 border rounded-md text-sm cursor-pointer transition-all duration-200 flex items-center gap-2 font-medium ${
                          isSelected 
                            ? "bg-[#1a7f4e] text-white border-[#1a7f4e]" 
                            : "bg-white text-[#333] border-[#e5e5e5] hover:border-[#1a7f4e] hover:bg-[#f0f9f4]"
                        }`}
                      >
                        {tag.label}
                        {isSelected && <span className="text-base">✓</span>}
                      </button>
                    )
                  })}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="flex gap-4 p-6 border-t border-[#e5e5e5] justify-end">
          <button
            onClick={() => {
              selectedTags.forEach(onTagToggle)
            }}
            className="py-3 px-6 bg-[#ef4444] border-none rounded-lg text-base font-semibold text-white cursor-pointer transition-all duration-200 hover:bg-[#dc2626] disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={selectedTags.length === 0}
          >
            Limpar Seleção ({selectedTags.length})
          </button>
          <button 
            className="py-3 px-6 bg-[#1a7f4e] border-none rounded-lg text-base font-semibold text-white cursor-pointer transition-all duration-200 hover:bg-[#156b42] hover:-translate-y-px hover:shadow-[0_2px_4px_rgba(26,127,78,0.2)] active:translate-y-0" 
            onClick={handleSave}
          >
            Salvar
          </button>
        </div>
      </div>
    </div>
  )
}