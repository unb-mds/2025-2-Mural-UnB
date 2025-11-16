import pytest
import json
import csv
import numpy as np 

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

    # 1.1: Finge um laboratório (lido do CSV)
    LAB_FALSO = [{
        'id': '200001', 'nome': 'Lab de Robótica', 'coordenador': 'Prof.', 
        'contato': 'email@unb.br', 'descricao': 'Este lab fala sobre robôs.'
    }]
    mocker.patch('scripts.alocar_tags_embeddings.carregar_laboratorios', return_value=LAB_FALSO)

    # 1.2: Finge tags com embeddings (lidas do JSON)
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

    # 1.3: Mock da API do Gemini (gerar_embedding para o LAB)
    VETOR_LAB_FALSO = np.array([0.9, 0.1, 0])
    mocker.patch('scripts.alocar_tags_embeddings.gerar_embedding', return_value=VETOR_LAB_FALSO)

    # 1.4: Mock do Sistema de Arquivos (para capturar a saída)
    mocker.patch('scripts.alocar_tags_embeddings.os.path.exists', return_value=True)
    mock_arquivo_saida = mocker.mock_open()
    mocker.patch('builtins.open', mock_arquivo_saida)

    # --- 2. ACT (Executar a Função) ---

    main() 


    # --- 3. ASSERT (Verificar o Resultado) ---

    # 3.1: O script tentou salvar o arquivo de saída correto?
    caminho_saida_esperado = os.path.join(
        os.path.dirname(scripts.alocar_tags_embeddings.__file__), 
        "..", "data", "Labs", "labs_com_tags_embeddings.json"
    )
    mock_arquivo_saida.assert_called_with(caminho_saida_esperado, 'w', encoding='utf-8')

    # 3.2: O script escreveu o JSON correto no arquivo?
    handle = mock_arquivo_saida()
    escrita_capturada = handle.write.call_args[0][0]
    json_escrito = json.loads(escrita_capturada)

    # 3.3: Verifica se a tag "Robótica" foi alocada (pois [0.9, 0.1, 0] é similar a [1, 0, 0])
    tags_alocadas = json_escrito['laboratorios'][0]['tags']
    assert len(tags_alocadas) > 0 # Deve ter encontrado pelo menos uma tag
    assert tags_alocadas[0]['id'] == 'robotica'

    # 3.4: Verifica se a tag "Software" (vetor [0, 1, 0]) foi filtrada (score baixo)
    ids_tags = [tag['id'] for tag in tags_alocadas]
    assert 'software' not in ids_tags