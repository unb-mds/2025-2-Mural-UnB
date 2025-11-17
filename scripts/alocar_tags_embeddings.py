"""
Script para alocar tags aos laboratórios usando EMBEDDINGS
Usa similaridade de cosseno entre embeddings das descrições e das tags

"""

import json
import csv
import os
import numpy as np
import google.generativeai as genai
from typing import List, Dict, Tuple

# Configuração da API do Gemini


def carregar_tags_com_embeddings(caminho_tags: str) -> Tuple[Dict, List[Dict]]:
    """
    Carrega as tags com embeddings do arquivo JSON
    
    Returns:
        (tags_data, lista_tags_flat)
        - tags_data: estrutura completa do JSON
        - lista_tags_flat: lista achatada de todas as tags com embeddings
    """
    with open(caminho_tags, 'r', encoding='utf-8') as f:
        tags_data = json.load(f)
    
    # Achata a estrutura para lista de tags
    tags_flat = []
    for categoria in tags_data['categorias']:
        for subcategoria in categoria['subcategorias']:
            for tag in subcategoria['tags']:
                if 'embedding' in tag and tag['embedding']:
                    tags_flat.append({
                        'id': tag['id'],
                        'label': tag['label'],
                        'description': tag['description'],
                        'embedding': np.array(tag['embedding']),
                        'categoria': categoria['nome_categoria'],
                        'subcategoria': subcategoria['nome_subcategoria']
                    })
    
    return tags_data, tags_flat

def carregar_laboratorios(caminho_csv: str) -> List[Dict]:
    """Carrega os laboratórios do CSV"""
    labs = []
    with open(caminho_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            labs.append({
                'id': row.get('id'),
                'nome': row['nome'],
                'coordenador': row['coordenador'],
                'contato': row['contato'],
                'descricao': row['descricao']
            })
    return labs

def gerar_embedding(texto: str, model_name: str = 'models/text-embedding-004') -> np.ndarray:
    """
    Gera embedding para um texto usando Gemini
    
    Args:
        texto: Texto para gerar embedding
        model_name: Nome do modelo de embedding
    
    Returns:
        Array numpy com o embedding
    """
    result = genai.embed_content(
        model=model_name,
        content=texto,
        task_type="retrieval_document"
    )
    return np.array(result['embedding'])

def similaridade_cosseno(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Calcula similaridade de cosseno entre dois embeddings
    
    Returns:
        Valor entre -1 e 1 (quanto maior, mais similar)
    """
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)

def filtrar_tags_para_laboratorios(tags_flat: List[Dict]) -> List[Dict]:
    """
    Filtra tags removendo aquelas específicas para Empresas Juniores.
    Laboratórios não devem receber tags de EJ, Startup, etc.
    """
    # Tags que NUNCA devem aparecer para Laboratórios
    tags_excluidas = [
        'empresa_junior',
        'equipe_competicao',
        'startup_universitaria',
        'estagio'
    ]
    
    tags_filtradas = [
        tag for tag in tags_flat
        if tag.get('id') not in tags_excluidas
    ]
    
    print(f"  ℹ️  Filtro para laboratórios: {len(tags_flat)} → {len(tags_filtradas)} tags")
    return tags_filtradas


def alocar_tags_por_similaridade(
    lab: Dict,
    tags_flat: List[Dict],
    threshold: float = 0.35,
    max_tags: int = None
) -> List[Dict]:
    """
    Aloca tags a um laboratório baseado em similaridade de embeddings
    
    Args:
        lab: Dicionário com informações do laboratório
        tags_flat: Lista de tags com embeddings
        threshold: Similaridade mínima para considerar a tag (0-1)
        max_tags: Número máximo de tags a alocar (None = sem limite)
    
    Returns:
        Lista de tags selecionadas com score de similaridade
    """
    # Cria texto completo do laboratório para embedding
    texto_lab = f"{lab['nome']}. {lab['descricao']}"
    
    print(f"  → Gerando embedding da descrição...")
    lab_embedding = gerar_embedding(texto_lab)
    
    # Filtra tags irrelevantes para laboratórios
    tags_relevantes = filtrar_tags_para_laboratorios(tags_flat)
    
    print(f"  → Calculando similaridades com {len(tags_relevantes)} tags...")
    # Calcula similaridade com todas as tags
    similaridades = []
    for tag in tags_relevantes:
        score = similaridade_cosseno(lab_embedding, tag['embedding'])
        if score >= threshold:
            similaridades.append({
                'id': tag['id'],
                'label': tag['label'],
                'description': tag['description'],
                'categoria': tag['categoria'],
                'subcategoria': tag['subcategoria'],
                'score': float(score)
            })
    
    # Ordena por similaridade (maior primeiro)
    similaridades.sort(key=lambda x: x['score'], reverse=True)
    
    # Aplica limite máximo se especificado
    if max_tags is not None:
        tags_selecionadas = similaridades[:max_tags]
    else:
        tags_selecionadas = similaridades
    
    if len(tags_selecionadas) > 0:
        print(f"  ✓ {len(tags_selecionadas)} tags selecionadas (scores: {tags_selecionadas[0]['score']:.3f} a {tags_selecionadas[-1]['score']:.3f})")
    else:
        print(f"  ⚠ Nenhuma tag encontrada com similaridade >= {threshold}")
    
    return tags_selecionadas


def main():
    """Função principal"""
    print("="*70)
    print("ALOCAÇÃO DE TAGS POR SIMILARIDADE DE EMBEDDINGS")
    print("="*70)
    print()
    
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        print("ERRO: Configure a variável de ambiente GEMINI_API_KEY")
        print("Execute: $env:GEMINI_API_KEY='sua-chave-aqui'")
        return

    genai.configure(api_key=GEMINI_API_KEY)

    # Caminhos dos arquivos
    script_dir = os.path.dirname(__file__)
    caminho_tags = os.path.join(script_dir, "..", "data", "tags.json")  # COM embeddings!
    caminho_csv = os.path.join(script_dir, "..", "data", "Labs", "labs_fga.csv")
    caminho_saida = os.path.join(script_dir, "..", "data", "Labs", "labs_com_tags_embeddings.json")
    
    # Verifica se arquivo de tags com embeddings existe
    if not os.path.exists(caminho_tags):
        print(f"❌ ERRO: Arquivo {caminho_tags} não encontrado!")
        print()
        print("Este script precisa do arquivo tags.json COM embeddings.")
        print("Execute primeiro: python generate_embeddings_gemini.py")
        return
    
    # Carrega dados
    tags_data, tags_flat = carregar_tags_com_embeddings(caminho_tags)
    laboratorios = carregar_laboratorios(caminho_csv)
    
    print(f"   • {len(laboratorios)} laboratórios carregados")
    print(f"   • {len(tags_flat)} tags com embeddings disponíveis")
    print()
    
    
    labs_com_tags = []
    
    for i, lab in enumerate(laboratorios, 1):
        print(f"\n[{i}/{len(laboratorios)}] {lab['nome'][:60]}...")
        
        # Aloca tags por similaridade
        tags_selecionadas = alocar_tags_por_similaridade(
            lab,
            tags_flat,
            threshold=0.35,  # Similaridade mínima de 35%
            max_tags=12  # Limita às 15 tags mais relevantes
        )        # Adiciona à lista (sem o score na saída final)
        tags_para_salvar = [
            {
                'id': tag['id'],
                'label': tag['label'],
                'categoria': tag['categoria'],
                'subcategoria': tag['subcategoria']
            }
            for tag in tags_selecionadas
        ]
        
        labs_com_tags.append({
            'id': lab.get('id', i), # fallback
            'nome': lab['nome'],
            'coordenador': lab['coordenador'],
            'contato': lab['contato'],
            'descricao': lab['descricao'],
            'tags': tags_para_salvar,
            'total_tags': len(tags_para_salvar),
            'top_tags_scores': [
                {'label': t['label'], 'score': round(t['score'], 3)}
                for t in tags_selecionadas[:3]
            ]
        })
        
        # Mostra preview das tags
        if tags_selecionadas:
            print(f"  Top 5 tags:")
            for tag in tags_selecionadas[:5]:
                print(f"    • {tag['label']} (score: {tag['score']:.3f})")
    
    print()
    print("-"*70)
    print()
    
    # Salva resultado
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump({
            'metodo': 'similaridade_embeddings',
            'modelo_embedding': 'text-embedding-004',
            'total_laboratorios': len(labs_com_tags),
            'data_geracao': '2025-10-20',
            'parametros': {
                'min_tags': 3,
                'max_tags': 12,
                'threshold_similaridade': 0.35
            },
            'laboratorios': labs_com_tags
        }, f, ensure_ascii=False, indent=2)
    

    
    # Estatísticas
    print(f"   • Total de laboratórios processados: {len(labs_com_tags)}")
    
    total_tags = sum(lab['total_tags'] for lab in labs_com_tags)
    media_tags = total_tags / len(labs_com_tags) if labs_com_tags else 0
    print(f"   • Total de tags alocadas: {total_tags}")
    print(f"   • Média de tags por laboratório: {media_tags:.1f}")
    


if __name__ == "__main__":
    main()
