"""
Agrega embeddings de tags para cada empresa júnior (média das embeddings das tags).
Lê lookup de tags, calcula embedding médio e salva resultado em JSON.
"""

import json
import numpy as np
import os

# Nomes dos arquivos
ARQUIVO_TAGS_MESTRE = '../data/tags.json'
ARQUIVO_EJS = '../data/EJs/empresas_juniores_com_tags_embeddings.json'
ARQUIVO_SAIDA = '../data/EJs/empresas_juniores_com_embedding_agregado.json'

def carregar_lookup_embeddings(filepath):
    """
    Carrega o arquivo mestre de tags e cria um dicionário
    mapeando tag_id -> embedding.
    """
    print(f"Carregando e processando '{filepath}'...")
    lookup = {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Navega pela estrutura aninhada para encontrar as tags
        for categoria in data.get('categorias', []):
            for subcategoria in categoria.get('subcategorias', []):
                for tag in subcategoria.get('tags', []):
                    if 'id' in tag and 'embedding' in tag:
                        lookup[tag['id']] = tag['embedding']
                        
        print(f"Total de {len(lookup)} tags carregadas no lookup.")
        return lookup
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar JSON em '{filepath}'. Verifique o formato.")
        return None

def processar_empresas_juniores(arquivo_ejs_path, lookup_embeddings):
    """
    Processa o arquivo de empresas juniores, calcula o embedding agregado
    e retorna a estrutura de dados atualizada.
    """
    print(f"Carregando arquivo de empresas juniores '{arquivo_ejs_path}'...")
    
    try:
        with open(arquivo_ejs_path, 'r', encoding='utf-8') as f:
            dados_ejs = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_ejs_path}' não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar JSON em '{arquivo_ejs_path}'.")
        return None

    empresas = dados_ejs.get('empresas_juniores', [])
    if not empresas:
        print("Aviso: Nenhuma empresa júnior encontrada no arquivo.")
        return dados_ejs

    print(f"Processando {len(empresas)} empresas juniores...")
    ejs_processadas = 0
    
    for ej in empresas:
        ej_id = ej.get('id', 'N/A')
        ej_nome = ej.get('Nome', 'N/A')
        tags_da_ej = ej.get('tags', [])
        
        embeddings_para_agregar = []
        
        for tag_info in tags_da_ej:
            tag_id = tag_info.get('id')
            if tag_id in lookup_embeddings:
                embeddings_para_agregar.append(lookup_embeddings[tag_id])
            else:
                print(f"  [Aviso] EJ {ej_id} ({ej_nome}): Tag ID '{tag_id}' não encontrada no lookup. Será ignorada.")
        
        # Calcula o embedding agregado (média dos embeddings)
        if embeddings_para_agregar:
            # Usa numpy para calcular a média de forma eficiente
            # axis=0 calcula a média ao longo das colunas (dimensões do embedding)
            embedding_medio = np.mean(embeddings_para_agregar, axis=0)
            
            # Converte o array numpy de volta para uma lista Python
            # para que possa ser salvo como JSON
            ej['embedding_agregado'] = embedding_medio.tolist()
            ejs_processadas += 1
        else:
            print(f"  [Aviso] EJ {ej_id} ({ej_nome}): Nenhuma tag válida encontrada. Embedding agregado não gerado.")
            ej['embedding_agregado'] = None # Ou [] se preferir

    print(f"\nProcessamento concluído. {ejs_processadas} empresas juniores tiveram embeddings agregados gerados.")
    return dados_ejs

def salvar_resultado(data, filepath):
    """
    Salva os dados processados em um novo arquivo JSON.
    """
    print(f"Salvando resultado em '{filepath}'...")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Arquivo salvo com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

# --- Execução Principal ---
if __name__ == "__main__":
    # Passo 1: Carregar o mapa de embeddings das tags
    lookup_de_embeddings = carregar_lookup_embeddings(ARQUIVO_TAGS_MESTRE)
    
    if lookup_de_embeddings:
        # Passo 2 e 3: Carregar e processar as empresas juniores
        dados_atualizados = processar_empresas_juniores(ARQUIVO_EJS, lookup_de_embeddings)
        
        if dados_atualizados:
            # Passo 4: Salvar o resultado
            salvar_resultado(dados_atualizados, ARQUIVO_SAIDA)
