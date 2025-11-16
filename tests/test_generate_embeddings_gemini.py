import pytest
import json
import os

# Importa o módulo (para mockar) e as funções (para chamar)
import scripts.generate_embeddings_gemini
from scripts.generate_embeddings_gemini import main, INPUT_JSON_FILE, OUTPUT_JSON_FILE


def test_generate_embeddings_sucesso(mocker):

    # --- 1. ARRANGE ---
    JSON_ENTRADA_FALSO = {
        "categorias": [{"nome_categoria": "Engenharia de Software", "subcategorias": [{"nome_subcategoria": "Desenvolvimento",
            "tags": [{"id": "tag1", "label": "Teste de Software", "description": "Testando..."}]
        }]}]
    }

    # 1.2: Mock de 'open' (CORRIGIDO)
    mock_open_geral = mocker.patch(
        "builtins.open", 
        mocker.mock_open(read_data=json.dumps(JSON_ENTRADA_FALSO))
    )

    # 1.3: Mock da API
    VETOR_FALSO = [0.1, 0.2, 0.3]
    mocker.patch(
        "scripts.generate_embeddings_gemini.get_embedding", return_value=VETOR_FALSO
    )
    mocker.patch("scripts.generate_embeddings_gemini.os.makedirs")
    # 1.5: Mock da API Key
    mocker.patch("scripts.generate_embeddings_gemini.os.getenv", return_value="FAKE_API_KEY")

    # --- 2. ACT ---
    main()

    # --- 3. ASSERT ---
    mock_open_geral.assert_any_call(INPUT_JSON_FILE, "r", encoding="utf-8")
    mock_open_geral.assert_any_call(OUTPUT_JSON_FILE, "w", encoding="utf-8")

    # 3.3: Captura a escrita (CORRIGIDO)
    handle_arquivo_falso = mock_open_geral()
    # Junta todas as chamadas 'write' em uma única string
    string_json_completa = "".join(chamada[1][0] for chamada in handle_arquivo_falso.write.mock_calls)
    json_escrito = json.loads(string_json_completa)

    tag_escrita = json_escrito["categorias"][0]["subcategorias"][0]["tags"][0]
    assert tag_escrita["embedding"] == VETOR_FALSO
    assert tag_escrita["id"] == "tag1"


def test_generate_embeddings_falha_api_gemini(mocker):
    # --- 1. ARRANGE ---
    JSON_ENTRADA_FALSO = {"categorias": [{"subcategorias": [{"tags": [{"id": "tag1", "label": "Teste de Software"}]}]}]}

    # 1.2: Mock de 'open'
    mock_open_geral = mocker.patch(
        "builtins.open",
        mocker.mock_open(read_data=json.dumps(JSON_ENTRADA_FALSO))
    )

    # 1.3: Mock da API para FALHAR
    mocker.patch(
        "scripts.generate_embeddings_gemini.get_embedding",
        side_effect=ValueError("Erro simulado da API"),
    )

    # 1.4: Mocks de OS
    mocker.patch("scripts.generate_embeddings_gemini.os.makedirs")
    mocker.patch("scripts.generate_embeddings_gemini.os.getenv", return_value="FAKE_API_KEY")

    # --- 2. ACT e 3. ASSERT ---
    
    # Verifica se o erro "ValueError" foi mesmo lançado
    with pytest.raises(ValueError, match="Erro simulado da API"):
        main() # Roda a função main()

    # Verifica se o arquivo de SAÍDA NUNCA foi aberto para escrita
    chamadas_open = mock_open_geral.call_args_list
    chamada_saida_encontrada = False
    for chamada in chamadas_open:
        if chamada[0][0] == OUTPUT_JSON_FILE:
            chamada_saida_encontrada = True
    assert chamada_saida_encontrada == False