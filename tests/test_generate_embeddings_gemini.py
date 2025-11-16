import pytest
import json
import os

import scripts.generate_embeddings_gemini
from scripts.generate_embeddings_gemini import main, INPUT_JSON_FILE, OUTPUT_JSON_FILE

def test_generate_embeddings_sucesso(mocker):
    
    # --- 1. ARRANGE (Preparar as "Mentiras"/Simulações) ---
    
    # 1.1: JSON de entrada falso (COM A ESTRUTURA CORRETA)
    JSON_ENTRADA_FALSO = {
        "categorias": [{
            "nome_categoria": "Engenharia de Software",
            "subcategorias": [{
                "nome_subcategoria": "Desenvolvimento",
                "tags": [
                    {"id": "tag1", "label": "Teste de Software", "description": "Testando..."}
                ]
            }]
        }]
    }
    
    # 1.2: Mock da leitura de arquivo ('open')
    mock_open_geral = mocker.patch(
        'builtins.open', 
        mocker.mock_open(read_data=json.dumps(JSON_ENTRADA_FALSO))
    )
    
    # 1.3: Mock da função get_embedding (que chama a API do Gemini)
    VETOR_FALSO = [0.1, 0.2, 0.3]
    mocker.patch(
        'scripts.generate_embeddings_gemini.get_embedding', 
        return_value=VETOR_FALSO
    )

    # 1.4: Mock do os.makedirs (o script tenta criar a pasta)
    mocker.patch('scripts.generate_embeddings_gemini.os.makedirs')
    
    
    # --- 2. ACT (Executar a Função) ---
    
    main() 
    
    
    # --- 3. ASSERT (Verificar o Resultado) ---
    
    # 3.1: O script tentou LER o arquivo de entrada correto?
    mock_open_geral.assert_any_call(INPUT_JSON_FILE, 'r', encoding='utf-8')
    
    # 3.2: O script tentou SALVAR o arquivo de saída correto?
    mock_open_geral.assert_any_call(OUTPUT_JSON_FILE, 'w', encoding='utf-8')

    # 3.3: O script escreveu o JSON correto no arquivo?
    handle_arquivo_falso = mock_open_geral()
    escrita_capturada = handle_arquivo_falso.write.call_args[0][0]
    json_escrito = json.loads(escrita_capturada)
    
    # 3.4: Verificamos o JSON de saída (COM A ESTRUTURA CORRETA)
    tag_escrita = json_escrito["categorias"][0]["subcategorias"][0]["tags"][0]
    assert tag_escrita["embedding"] == VETOR_FALSO
    assert tag_escrita["id"] == "tag1"


def test_generate_embeddings_falha_api_gemini(mocker):
    # --- 1. ARRANGE ---

    # JSON de entrada (necessário para a leitura)
    JSON_ENTRADA_FALSO = {
        "categorias": [{"subcategorias": [{"tags": [
            {"id": "tag1", "label": "Teste de Software", "description": "Testando..."}
        ]}]}]
    }
    mocker.patch(
        'builtins.open', 
        mocker.mock_open(read_data=json.dumps(JSON_ENTRADA_FALSO))
    )

    # Mock da função get_embedding PARA FALHAR
    mocker.patch(
    'scripts.generate_embeddings_gemini.get_embedding', 
    side_effect=ValueError("Erro simulado da API") 
    )

    # Mock do os.makedirs
    mocker.patch('scripts.generate_embeddings_gemini.os.makedirs')

    mock_arquivo_saida = mocker.mock_open()
    mocker.patch('builtins.open', mock_arquivo_saida)


    # --- 2. ACT ---

    main() 


    # --- 3. ASSERT ---

    chamadas_open = mock_arquivo_saida.call_args_list

    chamada_saida_encontrada = False
    for chamada in chamadas_open:
        if chamada[0][0] == OUTPUT_JSON_FILE:
            chamada_saida_encontrada = True

    assert chamada_saida_encontrada == False