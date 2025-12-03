import json
import os

SCRIPT_DIR = os.path.dirname(__file__)
ARQUIVO_LABS = os.path.join(SCRIPT_DIR, '..', 'data', 'Labs', 'labs_com_embedding_agregado.json')
ARQUIVO_EJS = os.path.join(SCRIPT_DIR, '..', 'data', 'EJs', 'empresas_juniores_com_embedding_agregado.json')
ARQUIVO_SAIDA = os.path.join(SCRIPT_DIR, '..', 'site', 'public', 'json', 'oportunidades.json')

def carregar_json(filepath):
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

def juntar_oportunidades(labs_data, ejs_data):
    """
    Junta os dados de laboratórios e empresas juniores em uma única estrutura
    mantendo listas separadas
    """
    print("\nJuntando dados...")
    
    # Extrai as listas
    laboratorios = labs_data.get('laboratorios', [])
    empresas_juniores = ejs_data.get('empresas_juniores', [])
    
    for lab in laboratorios:
        lab['tipo_oportunidade'] = 'laboratorio'
    
    for ej in empresas_juniores:
        ej['tipo_oportunidade'] = 'empresa_junior'
    
    # Cria a estrutura final com duas listas separadas
    resultado_oportunidades = {
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
    print(f"Total de {resultado_oportunidades['total_oportunidades']} oportunidades")
    
    return resultado_oportunidades

def salvar_json(data, filepath):
    print(f"\nSalvando resultado em '{filepath}'...")
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Arquivo salvo com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def main():
    print("="*70)
    print("JUNÇÃO DE LABORATÓRIOS E EMPRESAS JUNIORES")
    print("="*70)
    print()
    
    dados_labs = carregar_json(ARQUIVO_LABS)
    dados_ejs = carregar_json(ARQUIVO_EJS)
    
    if dados_labs and dados_ejs:
        oportunidades = juntar_oportunidades(dados_labs, dados_ejs)
        
        salvar_json(oportunidades, ARQUIVO_SAIDA)
        
        print("\n" + "="*70)
        print("PROCESSO CONCLUÍDO!")
        print("="*70)
    else:
        print("\nErro: Não foi possível carregar os arquivos necessários.")

if __name__ == "__main__":
    main()