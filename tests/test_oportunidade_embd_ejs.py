import json
import pytest
import numpy as np
import os
from unittest.mock import patch, mock_open, MagicMock
from scripts.oportunidade_embd_ejs import (
    carregar_lookup_embeddings,
    processar_empresas_juniores,
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
def mock_ejs_data():
    return {
        "empresas_juniores": [
            {
                "id": "ej1",
                "tags": [{"id": "tag1"}, {"id": "tag2"}]
            },
            {
                "id": "ej2",
                "tags": [{"id": "tag_inexistente"}]
            },
            {
                "id": "ej3",
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

def test_processar_empresas_juniores_sucesso(mock_ejs_data):
    lookup = {
        "tag1": [0.1, 0.2, 0.3],
        "tag2": [0.4, 0.5, 0.6]
    }
    json_str = json.dumps(mock_ejs_data)
    
    with patch("builtins.open", mock_open(read_data=json_str)):
        resultado = processar_empresas_juniores("fake_ejs.json", lookup)
        
        ej1 = resultado["empresas_juniores"][0]
        assert "embedding_agregado" in ej1
        np.testing.assert_almost_equal(ej1["embedding_agregado"], [0.25, 0.35, 0.45])

        ej2 = resultado["empresas_juniores"][1]
        assert ej2["embedding_agregado"] is None

        ej3 = resultado["empresas_juniores"][2]
        assert ej3["embedding_agregado"] is None

def test_processar_empresas_arquivo_inexistente():
    with patch("builtins.open", side_effect=FileNotFoundError):
        res = processar_empresas_juniores("nao_existe.json", {})
        assert res is None

def test_processar_empresas_json_invalido():
    with patch("builtins.open", mock_open(read_data="{ruim")):
        res = processar_empresas_juniores("ruim.json", {})
        assert res is None

def test_processar_empresas_sem_lista():
    with patch("builtins.open", mock_open(read_data=json.dumps({"outra_coisa": []}))):
        res = processar_empresas_juniores("vazio.json", {})
        assert "empresas_juniores" not in res


def test_salvar_resultado_sucesso():
    dados = {"teste": 123}
    with patch("builtins.open", mock_open()) as mock_file, \
         patch("os.makedirs"):
        salvar_resultado(dados, "saida.json")
        mock_file.assert_called_with("saida.json", 'w', encoding='utf-8')

def test_salvar_resultado_erro_io():
    with patch("builtins.open", side_effect=IOError("Erro de disco")), \
         patch("os.makedirs"):
        salvar_resultado({}, "saida.json")


def test_main_sucesso():
    
    with patch("scripts.oportunidade_embd_ejs.carregar_lookup_embeddings") as mock_carregar, \
         patch("scripts.oportunidade_embd_ejs.processar_empresas_juniores") as mock_processar, \
         patch("scripts.oportunidade_embd_ejs.salvar_resultado") as mock_salvar:
        
        mock_carregar.return_value = {"tag1": [1, 2]}
        mock_processar.return_value = {"ejs": []}
        
        main()
        
        mock_carregar.assert_called_once()
        mock_processar.assert_called_once()
        mock_salvar.assert_called_once()

def test_main_falha_carregar_lookup():
    with patch("scripts.oportunidade_embd_ejs.carregar_lookup_embeddings") as mock_carregar, \
         patch("scripts.oportunidade_embd_ejs.processar_empresas_juniores") as mock_processar, \
         patch("scripts.oportunidade_embd_ejs.salvar_resultado") as mock_salvar:
        
        mock_carregar.return_value = None 
        
        main()
        
        mock_carregar.assert_called_once()
        mock_processar.assert_not_called()
        mock_salvar.assert_not_called()

def test_main_falha_processar_ejs():
    with patch("scripts.oportunidade_embd_ejs.carregar_lookup_embeddings") as mock_carregar, \
         patch("scripts.oportunidade_embd_ejs.processar_empresas_juniores") as mock_processar, \
         patch("scripts.oportunidade_embd_ejs.salvar_resultado") as mock_salvar:
        
        mock_carregar.return_value = {"tag": [1]}
        mock_processar.return_value = None 
        
        main()
        
        mock_processar.assert_called_once()
        mock_salvar.assert_not_called()