import json
import pytest
import numpy as np
from unittest.mock import patch, mock_open, MagicMock
from scripts.oportunidade_embd import (
    carregar_lookup_embeddings,
    processar_laboratorios,
    salvar_resultado,
    main
)

@pytest.fixture
def mock_tags_data():
    return {
        "categorias": [
            {
                "subcategorias": [
                    {
                        "tags": [
                            {"id": "tag1", "embedding": [0.1, 0.2, 0.3]},
                            {"id": "tag2", "embedding": [0.4, 0.5, 0.6]}
                        ]
                    }
                ]
            }
        ]
    }

@pytest.fixture
def mock_labs_data():
    return {
        "laboratorios": [
            {
                "id": "lab1",
                "tags": [{"id": "tag1"}, {"id": "tag2"}]
            },
            {
                "id": "lab2",
                "tags": [{"id": "tag_inexistente"}]
            },
            {
                "id": "lab3",
                "tags": []
            }
        ]
    }

def test_carregar_lookup_sucesso(mock_tags_data):
    json_str = json.dumps(mock_tags_data)
    with patch("builtins.open", mock_open(read_data=json_str)):
        resultado = carregar_lookup_embeddings("fake_path.json")
        assert resultado is not None
        assert "tag1" in resultado
        assert resultado["tag1"] == [0.1, 0.2, 0.3]

def test_carregar_lookup_arquivo_nao_encontrado():
    with patch("builtins.open", side_effect=FileNotFoundError):
        resultado = carregar_lookup_embeddings("caminho_errado.json")
        assert resultado is None

def test_carregar_lookup_json_invalido():
    with patch("builtins.open", mock_open(read_data="{json ruim")):
        resultado = carregar_lookup_embeddings("arquivo_ruim.json")
        assert resultado is None

def test_processar_laboratorios_sucesso(mock_labs_data):
    lookup = {
        "tag1": [0.1, 0.2, 0.3],
        "tag2": [0.4, 0.5, 0.6]
    }
    json_str = json.dumps(mock_labs_data)
    
    with patch("builtins.open", mock_open(read_data=json_str)):
        resultado = processar_laboratorios("fake_labs.json", lookup)
        
        lab1 = resultado["laboratorios"][0]
        assert "embedding_agregado" in lab1
        np.testing.assert_almost_equal(lab1["embedding_agregado"], [0.25, 0.35, 0.45])

        lab2 = resultado["laboratorios"][1]
        assert lab2["embedding_agregado"] is None

        lab3 = resultado["laboratorios"][2]
        assert lab3["embedding_agregado"] is None

def test_processar_laboratorios_arquivo_inexistente():
    with patch("builtins.open", side_effect=FileNotFoundError):
        res = processar_laboratorios("nao_existe.json", {})
        assert res is None

def test_processar_laboratorios_sem_lista():
    with patch("builtins.open", mock_open(read_data=json.dumps({"outra_coisa": []}))):
        res = processar_laboratorios("vazio.json", {})
        assert res == {"outra_coisa": []}

def test_salvar_resultado_sucesso():
    dados = {"teste": 123}
    with patch("builtins.open", mock_open()) as mock_file:
        salvar_resultado(dados, "saida.json")
        mock_file.assert_called_with("saida.json", 'w', encoding='utf-8')

def test_salvar_resultado_erro_io():
    with patch("builtins.open", side_effect=IOError("Erro de disco")):
        salvar_resultado({}, "saida.json")

def test_main_sucesso():
    with patch("scripts.oportunidade_embd.carregar_lookup_embeddings") as mock_carregar, \
         patch("scripts.oportunidade_embd.processar_laboratorios") as mock_processar, \
         patch("scripts.oportunidade_embd.salvar_resultado") as mock_salvar:
        
        mock_carregar.return_value = {"tag1": [1, 2]}
        mock_processar.return_value = {"labs": []}
        
        main()
        
        mock_carregar.assert_called_once()
        mock_processar.assert_called_once()
        mock_salvar.assert_called_once()

def test_main_falha_carregar():
    with patch("scripts.oportunidade_embd.carregar_lookup_embeddings") as mock_carregar, \
         patch("scripts.oportunidade_embd.processar_laboratorios") as mock_processar, \
         patch("scripts.oportunidade_embd.salvar_resultado") as mock_salvar:
        
        mock_carregar.return_value = None
        
        main()
        
        mock_carregar.assert_called_once()
        mock_processar.assert_not_called()
        mock_salvar.assert_not_called()