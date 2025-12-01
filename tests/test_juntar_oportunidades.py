import json
import pytest
from unittest.mock import patch, mock_open
from scripts.juntar_oportunidades import (
    carregar_json,
    salvar_json,
    juntar_oportunidades,
    main
)

@pytest.fixture
def mock_dados_ejs():
    return {"empresas_juniores": [{"id": "ej1", "nome": "EJ Teste"}]}

@pytest.fixture
def mock_dados_labs():
    return {"laboratorios": [{"id": "lab1", "nome": "Lab Teste"}]}

def test_carregar_json_sucesso(mock_dados_ejs):
    json_str = json.dumps(mock_dados_ejs)
    with patch("builtins.open", mock_open(read_data=json_str)):
        dados = carregar_json("caminho/fake.json")
        assert dados == mock_dados_ejs

def test_carregar_json_erro_arquivo_nao_encontrado():
    with patch("builtins.open", side_effect=FileNotFoundError):
        dados = carregar_json("nao_existe.json")
        assert dados is None

def test_carregar_json_erro_json_invalido():
    with patch("builtins.open", mock_open(read_data="{json ruim")):
        dados = carregar_json("ruim.json")
        assert dados is None

def test_salvar_json_sucesso():
    dados = {"teste": 123}
    with patch("builtins.open", mock_open()) as mock_file, \
         patch("os.makedirs"):
        salvar_json(dados, "saida.json")
        mock_file.assert_called_with("saida.json", "w", encoding="utf-8")

def test_salvar_json_erro():
    with patch("builtins.open", side_effect=IOError("Erro disco")), \
         patch("os.makedirs"):
        salvar_json({}, "saida.json")

def test_juntar_oportunidades(mock_dados_ejs, mock_dados_labs):
    resultado = juntar_oportunidades(mock_dados_labs, mock_dados_ejs)
    assert "empresas_juniores" in resultado
    assert "laboratorios" in resultado
    assert resultado["laboratorios"][0]["tipo_oportunidade"] == "laboratorio"
    assert resultado["empresas_juniores"][0]["tipo_oportunidade"] == "empresa_junior"
    assert resultado["total_oportunidades"] == 2

def test_main_fluxo_completo(mock_dados_ejs, mock_dados_labs):
    with patch("scripts.juntar_oportunidades.carregar_json", side_effect=[mock_dados_labs, mock_dados_ejs]) as mock_carregar, \
         patch("scripts.juntar_oportunidades.salvar_json") as mock_salvar:
        
        main()
        
        assert mock_carregar.call_count == 2
        mock_salvar.assert_called_once()
        
        args, _ = mock_salvar.call_args
        dados_salvos = args[0]
        assert "empresas_juniores" in dados_salvos
        assert "laboratorios" in dados_salvos

def test_main_falha_carregamento():
    with patch("scripts.juntar_oportunidades.carregar_json", side_effect=[None, {}]) as mock_carregar, \
         patch("scripts.juntar_oportunidades.salvar_json") as mock_salvar:
        
        main()
        
        assert mock_carregar.call_count == 2
        mock_salvar.assert_not_called()