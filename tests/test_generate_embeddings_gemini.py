import pytest
import json
import os
from unittest.mock import MagicMock, patch, mock_open

# Importa o módulo (isso executa o código global, como load_dotenv)
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
    
    # Deve capturar a exceção e retornar None (imprimindo erro)
    with mocker.patch("builtins.print") as mock_print:
        emb = get_embedding("texto")
        assert emb is None
        assert mock_print.called

# --- Testes Unitários: process_tags ---

def test_process_tags_fluxo_completo(mocker):
    # Mock do get_embedding para retornar sucesso
    mocker.patch("scripts.generate_embeddings_gemini.get_embedding", return_value=[1.0, 1.0])
    
    # Dados com tags na raiz da categoria E em subcategorias
    dados = {
        "categorias": [
            {
                "nome": "Cat1",
                "tags": [{"id": "t1", "label": "Tag1", "description": "D1"}], # Caso 1
                "subcategorias": []
            },
            {
                "nome": "Cat2",
                "subcategorias": [
                    {
                        "tags": [
                            {"id": "t2", "label": "Tag2", "description": "D2"}, # Caso 2
                            {"id": "t3", "embedding": [0.1]} # Já tem embedding (deve pular)
                        ]
                    }
                ]
            }
        ]
    }
    
    resultado = process_tags(dados)
    
    # Tag1 deve ter ganho embedding
    assert resultado["categorias"][0]["tags"][0]["embedding"] == [1.0, 1.0]
    # Tag2 deve ter ganho embedding
    assert resultado["categorias"][1]["subcategorias"][0]["tags"][0]["embedding"] == [1.0, 1.0]
    # Tag3 deve ter mantido o original (não chamou API)
    assert resultado["categorias"][1]["subcategorias"][0]["tags"][1]["embedding"] == [0.1]

# --- Testes de Integração: main ---

def test_main_sucesso(mocker):
    # Mock de ambiente e arquivos
    mocker.patch("os.makedirs")
    mocker.patch("scripts.generate_embeddings_gemini.process_tags", return_value={"dados": "processados"})
    
    # Mock leitura e escrita
    mock_file = mocker.mock_open(read_data='{"dados": "originais"}')
    mocker.patch("builtins.open", mock_file)
    
    main()
    
    # Verifica leitura
    mock_file.assert_any_call(INPUT_JSON_FILE, "r", encoding="utf-8")
    # Verifica escrita
    mock_file.assert_any_call(OUTPUT_JSON_FILE, "w", encoding="utf-8")

def test_main_arquivo_entrada_nao_encontrado(mocker):
    mocker.patch("os.makedirs")
    mocker.patch("builtins.open", side_effect=FileNotFoundError)
    
    with mocker.patch("builtins.print") as mock_print:
        main()
        assert any("não encontrado" in str(c) for c in mock_print.mock_calls)

def test_main_json_invalido(mocker):
    mocker.patch("os.makedirs")
    mocker.patch("builtins.open", mock_open(read_data="{json ruim"))
    
    with mocker.patch("builtins.print") as mock_print:
        main()
        assert any("JSON válido" in str(c) for c in mock_print.mock_calls)

def test_main_erro_escrita(mocker):
    mocker.patch("os.makedirs")
    # Leitura OK, Escrita Falha
    mock_file = mocker.mock_open(read_data='{}')
    mock_file.side_effect = [mock_file.return_value, IOError("Disco cheio")] # 1ª chamada OK, 2ª Falha
    
    mocker.patch("builtins.open", mock_file)
    mocker.patch("scripts.generate_embeddings_gemini.process_tags", return_value={})
    
    with mocker.patch("builtins.print") as mock_print:
        main()
        assert any("Não foi possível escrever" in str(c) for c in mock_print.mock_calls)