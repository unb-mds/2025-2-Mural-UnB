"""
Script para alocar tags às Empresas Juniores usando EMBEDDINGS
Usa similaridade de cosseno entre embeddings das descrições e das tags 

"""

import json
import os
from typing import List, Dict, Tuple
import numpy as np
import google.generativeai as genai

# Configuração da API do Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("ERRO: Configure a variável de ambiente GEMINI_API_KEY")
    print("Execute: $env:GEMINI_API_KEY='sua-chave-aqui'")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)


def carregar_tags_com_embeddings(caminho_tags: str) -> Tuple[Dict, List[Dict]]:
    """
    Carrega as tags com embeddings do arquivo JSON
    Retorna (tags_data, lista_tags_flat)
    """
    with open(caminho_tags, 'r', encoding='utf-8') as f:
        tags_data = json.load(f)

    tags_flat = []
    for categoria in tags_data.get('categorias', []):
        for subcategoria in categoria.get('subcategorias', []):
            for tag in subcategoria.get('tags', []):
                if 'embedding' in tag and tag['embedding']:
                    tags_flat.append({
                        'id': tag.get('id'),
                        'label': tag.get('label'),
                        'description': tag.get('description'),
                        'embedding': np.array(tag['embedding']),
                        'categoria': categoria.get('nome_categoria'),
                        'subcategoria': subcategoria.get('nome_subcategoria')
                    })

    return tags_data, tags_flat


def carregar_empresas_juniores(caminho_json: str) -> List[Dict]:
    """Carrega empresas juniores de `empresas_juniores_consolidadas.json`"""
    with open(caminho_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('empresas_juniores', [])


def gerar_embedding(texto: str, model_name: str = 'models/text-embedding-004') -> np.ndarray:
    """
    Gera embedding para um texto usando Gemini
    """
    result = genai.embed_content(
        model=model_name,
        content=texto,
        task_type="retrieval_document"
    )
    return np.array(result['embedding'])


def similaridade_cosseno(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def alocar_tags_por_similaridade(
    empresa: Dict,
    tags_flat: List[Dict],
    min_tags: int = 5,
    max_tags: int = 15,
    threshold: float = 0.28
) -> List[Dict]:
    """Aloca tags a uma empresa baseada em similaridade de embeddings"""

    # Monta texto a partir dos campos mais relevantes (alguns podem estar ausentes)
    nome = empresa.get('Nome', '')
    sobre = empresa.get('Sobre', '')
    servicos = empresa.get('Servicos', '')
    missao = empresa.get('Missao', '')
    visao = empresa.get('Visao', '')

    texto = f"{nome}. {sobre} Serviços: {servicos} Missão: {missao} Visão: {visao}"

    print(f"  → Gerando embedding para: {nome[:60]}")
    emb = gerar_embedding(texto)

    similaridades = []
    print(f"  → Calculando similaridade com {len(tags_flat)} tags...")
    for tag in tags_flat:
        score = similaridade_cosseno(emb, tag['embedding'])
        if score >= threshold:
            similaridades.append({
                'id': tag['id'],
                'label': tag['label'],
                'description': tag.get('description'),
                'categoria': tag.get('categoria'),
                'subcategoria': tag.get('subcategoria'),
                'score': float(score)
            })

    similaridades.sort(key=lambda x: x['score'], reverse=True)

    num_tags = min(max_tags, max(min_tags, len(similaridades)))
    selecionadas = similaridades[:num_tags]

    if selecionadas:
        print(f"  ✓ Selecionadas {len(selecionadas)} tags (top score {selecionadas[0]['score']:.3f})")
    else:
        print(f"  ⚠️  Nenhuma tag acima do threshold ({threshold}). Será retornado vazio.")

    return selecionadas


def main():

    script_dir = os.path.dirname(__file__)
    caminho_tags = os.path.join(script_dir, '..', 'data', 'tags.json')
    caminho_ejs = os.path.join(script_dir, '..', 'data', 'EJs', 'empresas_juniores_consolidadas.json')
    caminho_saida = os.path.join(script_dir, '..', 'data', 'EJs', 'empresas_juniores_com_tags_embeddings.json')

    if not os.path.exists(caminho_tags):
        print(f"ERRO: arquivo de tags não encontrado: {caminho_tags}")
        print("Certifique-se de que `data/tags.json` contém embeddings (execute generate_embeddings_gemini.py)")
        return

    if not os.path.exists(caminho_ejs):
        print(f"ERRO: arquivo de EJs não encontrado: {caminho_ejs}")
        return

    _, tags_flat = carregar_tags_com_embeddings(caminho_tags)
    empresas = carregar_empresas_juniores(caminho_ejs)

    print(f"  {len(empresas)} empresas carregadas")
    print(f"  {len(tags_flat)} tags com embeddings disponíveis")

    resultado = []

    for i, empresa in enumerate(empresas, start=1):
        nome = empresa.get('Nome', f'Empresa_{i}')
        print(f"\n[{i}/{len(empresas)}] {nome[:70]}")

        tags_sel = alocar_tags_por_similaridade(
            empresa,
            tags_flat,
            min_tags=5,
            max_tags=15,
            threshold=0.45
        )

        tags_para_salvar = [
            {
                'id': t['id'],
                'label': t['label'],
                'categoria': t.get('categoria'),
                'subcategoria': t.get('subcategoria')
            }
            for t in tags_sel
        ]

        resultado.append({
            'id': empresa.get('id', i),
            'Nome': nome,
            'Cursos': empresa.get('Cursos'),
            'Site': empresa.get('Site'),
            'Instagram': empresa.get('Instagram'),
            'tags': tags_para_salvar,
            'total_tags': len(tags_para_salvar),
            'top_tags_scores': [
                {'label': t['label'], 'score': round(t['score'], 3)}
                for t in tags_sel[:3]
            ]
        })

    # Salva arquivo de saída
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump({
            'metodo': 'similaridade_embeddings',
            'modelo_embedding': 'text-embedding-004',
            'total_empresas': len(resultado),
            'data_geracao': '2025-11-09',
            'parametros': {
                'min_tags': 5,
                'max_tags': 15,
                'threshold_similaridade': 0.45
            },
            'empresas_juniores': resultado
        }, f, ensure_ascii=False, indent=2)

    # Estatísticas simples
    total_tags = sum(e['total_tags'] for e in resultado)
    media = total_tags / len(resultado) if resultado else 0
    print('\n' + '-'*70)
    print(f"   • Total de empresas processadas: {len(resultado)}")
    print(f"   • Total de tags alocadas: {total_tags}")
    print(f"   • Média de tags por empresa: {media:.1f}")


if __name__ == '__main__':
    main()
