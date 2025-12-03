import pytest
import json
import csv
import numpy as np 
import os
from unittest.mock import MagicMock, patch, mock_open

import scripts.alocar_tags_embeddings
from scripts.alocar_tags_embeddings import (
    main,
    similaridade_cosseno,
    alocar_tags_por_similaridade,
    gerar_embedding,
    carregar_laboratorios,
    carregar_tags_com_embeddings,
    filtrar_tags_para_laboratorios
)

# --- Fixtures ---
@pytest.fixture
def mock_tags_data():
    return {
        "categorias": [
            {
                "nome_categoria": "Cat1",
                "subcategorias": [
                    {
                        "nome_subcategoria": "Sub1",
                        "tags": [
                            {"id": "tag1", "label": "Tag 1", "description": "Desc1", "embedding": [0.1, 0.2, 0.3]},
                            {"id": "empresa_junior", "label": "EJ", "description": "EJ", "embedding": [0.1, 0.1, 0.1]}
                        ]
                    }
                ]
            }
        ]
    }

@pytest.fixture
def mock_csv_content():
    return "id,nome,coordenador,contato,descricao\n1,Lab1,Prof A,contato@a.com,Descricao do Lab 1"

# --- Testes Unitários de Funções Auxiliares ---

def test_similaridade_cosseno():
    v1 = np.array([1, 0, 0])
    v2 = np.array([1, 0, 0])
    assert similaridade_cosseno(v1, v2) == pytest.approx(1.0)
    
    v3 = np.array([1, 0, 0])
    v4 = np.array([0, 1, 0])
    assert similaridade_cosseno(v3, v4) == pytest.approx(0.0)
    
    v5 = np.array([0, 0, 0])
    assert similaridade_cosseno(v1, v5) == 0.0

def test_filtrar_tags_para_laboratorios():
    tags = [
        {'id': 'robotica', 'label': 'Robótica'},
        {'id': 'empresa_junior', 'label': 'EJ'},
        {'id': 'equipe_competicao', 'label': 'Equipe'},
        {'id': 'python', 'label': 'Python'}
    ]
    
    filtradas = filtrar_tags_para_laboratorios(tags)
    
    assert len(filtradas) == 2
    ids = [t['id'] for t in filtradas]
    assert 'robotica' in ids
    assert 'python' in ids
    assert 'empresa_junior' not in ids

# --- Testes de Carregamento de Arquivos ---

def test_carregar_tags_com_embeddings(mock_tags_data):
    json_str = json.dumps(mock_tags_data)
    with patch("builtins.open", mock_open(read_data=json_str)):
        data, flat_list = carregar_tags_com_embeddings("dummy.json")
        
        assert data == mock_tags_data
        assert len(flat_list) == 2
        assert isinstance(flat_list[0]['embedding'], np.ndarray)

def test_carregar_laboratorios(mock_csv_content):
    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        labs = carregar_laboratorios("dummy.csv")
        
        assert len(labs) == 1
        assert labs[0]['nome'] == 'Lab1'
        assert labs[0]['coordenador'] == 'Prof A'

# --- Teste de Geração de Embedding ---

def test_gerar_embedding(mocker):
    mock_genai = mocker.patch("scripts.alocar_tags_embeddings.genai")
    mock_genai.embed_content.return_value = {'embedding': [0.1, 0.2, 0.3]}
    
    emb = gerar_embedding("texto teste")
    
    assert isinstance(emb, np.ndarray)
    assert np.array_equal(emb, np.array([0.1, 0.2, 0.3]))

# --- Teste de Alocação ---

def test_alocar_tags_por_similaridade(mocker):
    mocker.patch("scripts.alocar_tags_embeddings.gerar_embedding", return_value=np.array([1, 0, 0]))
    
    lab = {'nome': 'Lab Teste', 'descricao': 'Desc'}
    tags = [
        {'id': 't1', 'label': 'T1', 'embedding': np.array([1, 0, 0]), 'categoria': 'C', 'subcategoria': 'S', 'description': 'D'},
        {'id': 't2', 'label': 'T2', 'embedding': np.array([0, 1, 0]), 'categoria': 'C', 'subcategoria': 'S', 'description': 'D'}
    ]
    
    selecionadas = alocar_tags_por_similaridade(lab, tags, threshold=0.5)
    
    assert len(selecionadas) == 1
    assert selecionadas[0]['id'] == 't1'
    assert selecionadas[0]['score'] > 0.9

    selecionadas_vazia = alocar_tags_por_similaridade(lab, tags, threshold=1.1)
    assert len(selecionadas_vazia) == 0

# --- Testes da Main (CORRIGIDO) ---

def test_main_sucesso(mocker):
    mocker.patch("os.environ.get", return_value="FAKE_KEY")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("scripts.alocar_tags_embeddings.genai.configure")
    
    mocker.patch("scripts.alocar_tags_embeddings.carregar_tags_com_embeddings", return_value=({}, []))
    
    # CORREÇÃO: O mock do laboratório agora tem todos os campos que o script acessa
    lab_mock = {
        'id': '1', 
        'nome': 'Lab1', 
        'descricao': 'D',
        'coordenador': 'Prof X',
        'contato': 'email',
    }
    mocker.patch("scripts.alocar_tags_embeddings.carregar_laboratorios", return_value=[lab_mock])
    
    mocker.patch("scripts.alocar_tags_embeddings.alocar_tags_por_similaridade", return_value=[])
    
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)
    
    main()
    
    handle = mock_file()
    assert handle.write.called

def test_main_sem_api_key(mocker):
    mocker.patch("os.environ.get", return_value=None)
    
    # CORREÇÃO: Patch direto sem 'with'
    mock_print = mocker.patch("builtins.print")
    
    main()
    
    # Verifica se chamou print com a mensagem de erro esperada
    # Usamos uma verificação mais flexível procurando a string na chamada
    assert any("ERRO: Configure a variável de ambiente" in str(call) for call in mock_print.mock_calls)

def test_main_arquivo_tags_nao_existe(mocker):
    mocker.patch("os.environ.get", return_value="KEY")
    mocker.patch("os.path.exists", side_effect=[False, True]) 
    
    # CORREÇÃO: Patch direto sem 'with'
    mock_print = mocker.patch("builtins.print")
    
    main()
    
    assert any("não encontrado" in str(call) for call in mock_print.mock_calls)