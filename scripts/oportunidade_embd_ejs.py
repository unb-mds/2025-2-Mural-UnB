"""
Agrega embeddings de tags para cada empresa júnior (média das embeddings das tags).
Lê lookup de tags, calcula embedding médio e salva resultado em JSON.
"""

import json
import numpy as np

# Nomes dos arquivos (Usando caminhos absolutos baseados no script)
SCRIPT_DIR = os.path.dirname(__file__)
ARQUIVO_TAGS_MESTRE = os.path.join(SCRIPT_DIR, '../data/tags.json')
ARQUIVO_EJS = os.path.join(SCRIPT_DIR, '../data/EJs/empresas_juniores_com_tags_embeddings.json')
ARQUIVO_SAIDA = os.path.join(SCRIPT_DIR, '../data/EJs/empresas_juniores_com_embedding_agregado.json')

def carregar_lookup_embeddings(filepath):
    """Carrega o arquivo mestre de tags e cria um dicionário mapeando tag_id -> embedding."""
    print(f"Carregando e processando '{filepath}'...")
    lookup = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
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
    """Calcula o embedding agregado para cada empresa júnior."""
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
        tags_da_ej = ej.get('tags', [])
        embeddings_para_agregar = []
        
        for tag_info in tags_da_ej:
            tag_id = tag_info.get('id')
            if tag_id in lookup_embeddings:
                embeddings_para_agregar.append(lookup_embeddings[tag_id])
            else:
                print(f"  [Aviso] EJ {ej_id}: Tag ID '{tag_id}' não encontrada no lookup.")
        
        if embeddings_para_agregar:
            embedding_medio = np.mean(embeddings_para_agregar, axis=0)
            ej['embedding_agregado'] = embedding_medio.tolist()
            ejs_processadas += 1
        else:
            print(f"  [Aviso] EJ {ej_id}: Nenhuma tag válida encontrada.")
            ej['embedding_agregado'] = None

    print(f"\nProcessamento concluído. {ejs_processadas} EJs com embeddings gerados.")
    return dados_ejs

def salvar_resultado(data, filepath):
    """Salva os dados processados."""
    print(f"Salvando resultado em '{filepath}'...")
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Arquivo salvo com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def main():
    print("="*70)
    print("AGREGAÇÃO DE EMBEDDINGS DE EJs")
    print("="*70)
    print()
    
    lookup_de_embeddings = carregar_lookup_embeddings(ARQUIVO_TAGS_MESTRE)
    
    if lookup_de_embeddings:
        dados_atualizados = processar_empresas_juniores(ARQUIVO_EJS, lookup_de_embeddings)
        
        if dados_atualizados:
            salvar_resultado(dados_atualizados, ARQUIVO_SAIDA)

if __name__ == "__main__":
    main()