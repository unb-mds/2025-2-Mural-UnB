// Um vetor de embedding é apenas um array de números
export type Embedding = number[];

// Interface para uma Tag individual (do tags.json)
export interface ITag {
  id: string;
  label: string;
  description: string;
  embedding: Embedding;
}

// Interface para a estrutura aninhada de tags.json
export interface ITagSubCategoria {
  nome_subcategoria: string;
  tags: ITag[];
}

export interface ITagCategoria {
  nome_categoria: string;
  descricao: string;
  subcategorias: ITagSubCategoria[];
}

// Interface para o arquivo mestre de tags
export interface ITagsData {
  categorias: ITagCategoria[];
}

// Interface para um Laboratório
export interface ILab {
  id: number;
  nome: string;
  coordenador: string;
  descricao: string;
  tags: Array<{ id: string; label: string }>;
  embedding_agregado: Embedding; // O mais importante!
  // ...outros campos que você queira usar
}

// Interface para o arquivo de laboratórios
export interface ILabsData {
  laboratorios: ILab[];
  // ...outros metadados
}

// Interface para o resultado da busca
export interface ISearchResult {
  lab: ILab;
  similarity: number;
}