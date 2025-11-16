"""
Agrega embeddings de tags para cada laboratório (média das embeddings das tags).
Lê lookup de tags, calcula embedding médio e salva resultado em JSON.
"""

import json
import numpy as np

# Nomes dos arquivos
ARQUIVO_TAGS_MESTRE = './data/tags.json'
ARQUIVO_LABS = './data/Labs/labs_com_tags_embeddings.json' 
ARQUIVO_SAIDA = './data/Labs/labs_com_embedding_agregado.json'

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

def processar_laboratorios(arquivo_labs_path, lookup_embeddings):
    """
    Processa o arquivo de laboratórios, calcula o embedding agregado
    e retorna a estrutura de dados atualizada.
    """
    print(f"Carregando arquivo de laboratórios '{arquivo_labs_path}'...")
    
    try:
        with open(arquivo_labs_path, 'r', encoding='utf-8') as f:
            dados_labs = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_labs_path}' não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar JSON em '{arquivo_labs_path}'.")
        return None

    laboratorios = dados_labs.get('laboratorios', [])
    if not laboratorios:
        print("Aviso: Nenhum laboratório encontrado no arquivo.")
        return dados_labs

    print(f"Processando {len(laboratorios)} laboratórios...")
    labs_processados = 0
    
    for lab in laboratorios:
        lab_id = lab.get('id', 'N/A')
        tags_do_lab = lab.get('tags', [])
        
        embeddings_para_agregar = []
        
        for tag_info in tags_do_lab:
            tag_id = tag_info.get('id')
            if tag_id in lookup_embeddings:
                embeddings_para_agregar.append(lookup_embeddings[tag_id])
            else:
                print(f"  [Aviso] Lab {lab_id}: Tag ID '{tag_id}' não encontrada no lookup. Será ignorada.")
        
        # Calcula o embedding agregado (média dos embeddings)
        if embeddings_para_agregar:
            # Usa numpy para calcular a média de forma eficiente
            # axis=0 calcula a média ao longo das colunas (dimensões do embedding)
            embedding_medio = np.mean(embeddings_para_agregar, axis=0)
            
            # Converte o array numpy de volta para uma lista Python
            # para que possa ser salvo como JSON
            lab['embedding_agregado'] = embedding_medio.tolist()
            labs_processados += 1
        else:
            print(f"  [Aviso] Lab {lab_id}: Nenhuma tag válida encontrada. Embedding agregado não gerado.")
            lab['embedding_agregado'] = None # Ou [] se preferir

    print(f"\nProcessamento concluído. {labs_processados} laboratórios tiveram embeddings agregados gerados.")
    return dados_labs

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
        # Passo 2 e 3: Carregar e processar os laboratórios
        dados_atualizados = processar_laboratorios(ARQUIVO_LABS, lookup_de_embeddings)
        
        if dados_atualizados:
            # Passo 4: Salvar o resultado
            salvar_resultado(dados_atualizados, ARQUIVO_SAIDA)