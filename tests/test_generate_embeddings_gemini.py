import pytest
import json

import scripts.generate_embeddings_gemini
from scripts.generate_embeddings_gemini import main

def test_generate_embeddings_sucesso(mocker):

    # --- 1. ARRANGE (Preparar as "Mentiras"/Simulações) ---

    # 1.1: JSON de entrada falso (o que fingimos ler)
    JSON_ENTRADA_FALSO = {
        "tags_sem_embedding": [
            {"id": "tag1", "label": "Teste de Software"}
        ]
    }

    # 1.2: Mock da leitura de arquivo ('open')
    mock_open_leitura = mocker.patch(
        'builtins.open', 
        mocker.mock_open(read_data=json.dumps(JSON_ENTRADA_FALSO))
    )

    # 1.3: Mock da API do Gemini (vamos fazer no próximo commit)
    VETOR_FALSO = [0.1, 0.2, 0.3, 0.4]
    mocker.patch(
        'scripts.generate_embeddings_gemini.get_embedding', 
        return_value=VETOR_FALSO
    )

    # 1.4: Mock da escrita de arquivo ('open')
    mock_arquivo_saida = mocker.mock_open()
    mocker.patch('builtins.open', mock_arquivo_saida)


    # --- 2. ACT (Executar a Função) ---

    main() 


    # --- 3. ASSERT (Verificar o Resultado) ---

    # 3.1: O script tentou salvar o arquivo no caminho correto?
    caminho_saida_esperado = 'data/mock/tags_with_embeddings_gemini.json'
    mock_open.assert_called_with(caminho_saida_esperado, 'w', encoding='utf-8')

    # 3.2: O script escreveu o JSON correto no arquivo?
    handle = mock_arquivo_saida()
    escrita_capturada = handle.write.call_args[0][0]
    json_escrito = json.loads(escrita_capturada)

    assert json_escrito["tags"][0]["embedding"] == VETOR_FALSO
    assert json_escrito["tags"][0]["id"] == "tag1"