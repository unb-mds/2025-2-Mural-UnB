import pytest
import json
import os
from scripts.juntar_oportunidades import main, juntar_oportunidades

def test_juntar_oportunidades_logica_pura():
    """Testa apenas a função de mesclagem de dicionários"""
    labs = {'laboratorios': [{'nome': 'Lab A'}]}
    ejs = {'empresas_juniores': [{'nome': 'EJ B'}]}
    
    resultado = juntar_oportunidades(labs, ejs)
    
    assert resultado['total_oportunidades'] == 2
    assert resultado['laboratorios'][0]['tipo_oportunidade'] == 'laboratorio'
    assert resultado['empresas_juniores'][0]['tipo_oportunidade'] == 'empresa_junior'

def test_juntar_oportunidades_main_sucesso(mocker):
    """Testa o fluxo principal da função main com mocks de arquivo"""
    
    # Mocka a leitura (carregar_json)
    mock_dados_labs = {'laboratorios': [{'nome': 'Lab Teste'}]}
    mock_dados_ejs = {'empresas_juniores': [{'nome': 'EJ Teste'}]}
    

    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    mock_open.side_effect = [
        mocker.mock_open(read_data=json.dumps(mock_dados_labs)).return_value, # Leitura Labs
        mocker.mock_open(read_data=json.dumps(mock_dados_ejs)).return_value,  # Leitura EJs
        mocker.mock_open().return_value # Escrita
    ]
    

    mocker.patch('os.makedirs')
    

    main()
    
    assert mock_open.call_count == 3
    args, kwargs = mock_open.call_args_list[2]
    assert 'oportunidades.json' in args[0]
    assert args[1] == 'w'