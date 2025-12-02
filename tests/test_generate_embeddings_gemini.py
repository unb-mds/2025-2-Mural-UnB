import pytest
import json
import os
from unittest.mock import MagicMock, patch, mock_open

import scripts.generate_embeddings_gemini
from scripts.generate_embeddings_gemini import (
    main, 
    process_tags, 
    get_embedding, 
    INPUT_JSON_FILE, 
    OUTPUT_JSON_FILE
)

# --- Testes Unitários: get_embedding ---

def test_get_embedding_sucesso(mocker):
    mock_genai = mocker.patch("scripts.generate_embeddings_gemini.genai")
    mock_genai.embed_content.return_value = {"embedding": [0.1, 0.2]}
    
    emb = get_embedding("texto")
    assert emb == [0.1, 0.2]

def test_get_embedding_falha(mocker):
    mock_genai = mocker.patch("scripts.generate_embeddings_gemini.genai")
    mock_genai.embed_content.side_effect = Exception("Erro API")
    
    # CORREÇÃO: Patch direto
    mock_print = mocker.patch("builtins.print")
    
    emb = get_embedding("texto")
    assert emb is None
    assert mock_print.called

# --- Testes Unitários: process_tags ---

def test_process_tags_fluxo_completo(mocker):
    mocker.patch("scripts.generate_embeddings_gemini.get_embedding", return_value=[1.0, 1.0])
    
    dados = {
        "categorias": [
            {
                "nome": "Cat1",
                "tags": [{"id": "t1", "label": "Tag1", "description": "D1"}],
                "subcategorias": []
            },
            {
                "nome": "Cat2",
                "subcategorias": [
                    {
                        "tags": [
                            {"id": "t2", "label": "Tag2", "description": "D2"},
                            {"id": "t3", "embedding": [0.1]}
                        ]
                    }
                ]
            }
        ]
    }
    
    resultado = process_tags(dados)
    
    assert resultado["categorias"][0]["tags"][0]["embedding"] == [1.0, 1.0]
    assert resultado["categorias"][1]["subcategorias"][0]["tags"][0]["embedding"] == [1.0, 1.0]
    assert resultado["categorias"][1]["subcategorias"][0]["tags"][1]["embedding"] == [0.1]

# --- Testes de Integração: main ---

def test_main_sucesso(mocker):
    mocker.patch("os.makedirs")
    mocker.patch("scripts.generate_embeddings_gemini.process_tags", return_value={"dados": "processados"})
    
    mock_file = mocker.mock_open(read_data='{"dados": "originais"}')
    mocker.patch("builtins.open", mock_file)
    
    main()
    
    mock_file.assert_any_call(INPUT_JSON_FILE, "r", encoding="utf-8")
    mock_file.assert_any_call(OUTPUT_JSON_FILE, "w", encoding="utf-8")

def test_main_arquivo_entrada_nao_encontrado(mocker):
    mocker.patch("os.makedirs")
    mocker.patch("builtins.open", side_effect=FileNotFoundError)
    
    mock_print = mocker.patch("builtins.print")
    
    main()
    assert any("não encontrado" in str(c) for c in mock_print.mock_calls)

def test_main_json_invalido(mocker):
    mocker.patch("os.makedirs")
    mocker.patch("builtins.open", mock_open(read_data="{json ruim"))
    
    mock_print = mocker.patch("builtins.print")
    
    main()
    assert any("JSON válido" in str(c) for c in mock_print.mock_calls)

def test_main_erro_escrita(mocker):
    mocker.patch("os.makedirs")
    mock_file = mocker.mock_open(read_data='{}')
    mock_file.side_effect = [mock_file.return_value, IOError("Disco cheio")]
    
    mocker.patch("builtins.open", mock_file)
    mocker.patch("scripts.generate_embeddings_gemini.process_tags", return_value={})
    
    mock_print = mocker.patch("builtins.print")
    
    main()
    assert any("Não foi possível escrever" in str(c) for c in mock_print.mock_calls)