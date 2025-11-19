"""
Junta os JSONs de laboratórios e empresas juniores em um único arquivo oportunidades.json
"""

import json
import os

# Caminhos dos arquivos
ARQUIVO_LABS = '../data/Labs/labs_com_embedding_agregado.json'
ARQUIVO_EJS = '../data/EJs/empresas_juniores_com_embedding_agregado.json'
ARQUIVO_SAIDA = '../site/public/json/oportunidades.json'

def carregar_json(filepath):
    """Carrega um arquivo JSON"""
    print(f"Carregando '{filepath}'...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar JSON em '{filepath}'.")
        return None

def juntar_oportunidades(dados_labs, dados_ejs):
    """
    Junta os dados de laboratórios e empresas juniores em uma única estrutura
    mantendo listas separadas
    """
    print("\nJuntando dados...")
    
    # Extrai as listas
    laboratorios = dados_labs.get('laboratorios', [])
    empresas_juniores = dados_ejs.get('empresas_juniores', [])
    
    # Adiciona tipo de oportunidade a cada item
    for lab in laboratorios:
        lab['tipo_oportunidade'] = 'laboratorio'
    
    for ej in empresas_juniores:
        ej['tipo_oportunidade'] = 'empresa_junior'
    
    # Cria a estrutura final com duas listas separadas
    oportunidades = {
        'metodo': 'similaridade_embeddings',
        'modelo_embedding': 'text-embedding-004',
        'total_oportunidades': len(laboratorios) + len(empresas_juniores),
        'total_laboratorios': len(laboratorios),
        'total_empresas_juniores': len(empresas_juniores),
        'laboratorios': laboratorios,
        'empresas_juniores': empresas_juniores
    }
    
    print(f"Total de {len(laboratorios)} laboratórios")
    print(f"Total de {len(empresas_juniores)} empresas juniores")
    print(f"Total de {oportunidades['total_oportunidades']} oportunidades")
    
    return oportunidades

def salvar_json(data, filepath):
    """Salva os dados em um arquivo JSON"""
    print(f"\nSalvando resultado em '{filepath}'...")
    try:
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Arquivo salvo com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

# --- Execução Principal ---
if __name__ == "__main__":
    print("="*70)
    print("JUNÇÃO DE LABORATÓRIOS E EMPRESAS JUNIORES")
    print("="*70)
    print()
    
    # Carrega os arquivos
    dados_labs = carregar_json(ARQUIVO_LABS)
    dados_ejs = carregar_json(ARQUIVO_EJS)
    
    if dados_labs and dados_ejs:
        # Junta os dados
        oportunidades = juntar_oportunidades(dados_labs, dados_ejs)
        
        # Salva o resultado
        salvar_json(oportunidades, ARQUIVO_SAIDA)
        
        print("\n" + "="*70)
        print("PROCESSO CONCLUÍDO!")
        print("="*70)
    else:
        print("\nErro: Não foi possível carregar os arquivos necessários.")
