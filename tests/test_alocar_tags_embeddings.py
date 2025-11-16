import pytest
import json
import csv
import numpy as np 
import os

import scripts.alocar_tags_embeddings
from scripts.alocar_tags_embeddings import (
    main,
    similaridade_cosseno,
    alocar_tags_por_similaridade,
    gerar_embedding,
    carregar_laboratorios,
    carregar_tags_com_embeddings
)


def test_similaridade_cosseno_vetores_identicos():
    """Testa se vetores idênticos retornam similaridade 1.0"""
    v1 = np.array([1, 2, 3])
    v2 = np.array([1, 2, 3])
    assert similaridade_cosseno(v1, v2) == pytest.approx(1.0)

def test_similaridade_cosseno_vetores_ortogonais():
    """Testa se vetores ortogonais (90 graus) retornam 0.0"""
    v1 = np.array([1, 0, 0])
    v2 = np.array([0, 1, 0])
    assert similaridade_cosseno(v1, v2) == pytest.approx(0.0)

def test_similaridade_cosseno_vetores_opostos():
    """Testa se vetores opostos retornam -1.0"""
    v1 = np.array([1, 2, 3])
    v2 = np.array([-1, -2, -3])
    assert similaridade_cosseno(v1, v2) == pytest.approx(-1.0)

def test_similaridade_cosseno_com_vetor_zero():
    """Testa se um vetor zero retorna 0.0"""
    v1 = np.array([1, 2, 3])
    v2 = np.array([0, 0, 0])
    assert similaridade_cosseno(v1, v2) == pytest.approx(0.0)


def test_alocar_tags_sucesso_completo(mocker):
    """
    Testa o fluxo principal: carregar labs, carregar tags,
    gerar embedding para o lab, calcular similaridade e salvar o JSON final.
    """

    # --- 1. ARRANGE (Preparar as "Mentiras"/Simulações) ---

    LAB_FALSO = [{
        'id': '200001', 'nome': 'Lab de Robótica', 'coordenador': 'Prof.', 
        'contato': 'email@unb.br', 'descricao': 'Este lab fala sobre robôs.'
    }]
    mocker.patch('scripts.alocar_tags_embeddings.carregar_laboratorios', return_value=LAB_FALSO)

    TAGS_FALSAS_FLAT = [
        {
            'id': 'robotica', 'label': 'Robótica', 'description': '...',
            'embedding': np.array([1, 0, 0]), # Vetor 1
            'categoria': 'Eng', 'subcategoria': 'Rob'
        },
        {
            'id': 'software', 'label': 'Software', 'description': '...',
            'embedding': np.array([0, 1, 0]), # Vetor 2
            'categoria': 'Eng', 'subcategoria': 'Soft'
        }
    ]
    mocker.patch('scripts.alocar_tags_embeddings.carregar_tags_com_embeddings', return_value=(None, TAGS_FALSAS_FLAT))

    VETOR_LAB_FALSO = np.array([0.9, 0.1, 0])
    mocker.patch('scripts.alocar_tags_embeddings.gerar_embedding', return_value=VETOR_LAB_FALSO)

    mocker.patch('scripts.alocar_tags_embeddings.os.path.exists', return_value=True)
    mocker.patch('scripts.alocar_tags_embeddings.os.environ.get', return_value="FAKE_API_KEY")
    
    mock_arquivo_saida = mocker.patch('builtins.open', mocker.mock_open())

    # --- 2. ACT (Executar a Função) ---
    main() 

    # --- 3. ASSERT (Verificar o Resultado) ---
    caminho_saida_esperado = os.path.join(
        os.path.dirname(scripts.alocar_tags_embeddings.__file__), 
        "..", "data", "Labs", "labs_com_tags_embeddings.json"
    )
    mock_arquivo_saida.assert_called_with(caminho_saida_esperado, 'w', encoding='utf-8')

    # CORREÇÃO AQUI: Junta todas as chamadas 'write' em uma única string
    handle = mock_arquivo_saida()
    string_json_completa = "".join(chamada[1][0] for chamada in handle.write.mock_calls)
    json_escrito = json.loads(string_json_completa)

    tags_alocadas = json_escrito['laboratorios'][0]['tags']
    assert len(tags_alocadas) > 0
    assert tags_alocadas[0]['id'] == 'robotica'

    ids_tags = [tag['id'] for tag in tags_alocadas]
    assert 'software' not in ids_tags