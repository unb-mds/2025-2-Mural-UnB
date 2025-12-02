import pytest
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from scripts.extrair_empresas_juniores import (
    configurar_ambiente,
    processar_pdf_empresas_juniores,
    consolidar_dados_empresas,
    mostrar_estatisticas_finais,
    main
)


def test_configurar_ambiente_sucesso():
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}), \
         patch('os.path.exists', return_value=False), \
         patch('os.makedirs') as mock_makedirs:
        
        assert configurar_ambiente() is True
        assert mock_makedirs.call_count == 2

def test_configurar_ambiente_sem_api_key():
    with patch('scripts.extrair_empresas_juniores.GEMINI_API_KEY', 'sua_chave_api_aqui'):
        assert configurar_ambiente() is False


def test_processar_pdf_download_necessario(mocker):
    mock_processor = mocker.Mock()
    mock_processor.processar_pdf_paginado.return_value = [{"Nome": "EJ"}]
    mock_processor.extrair_imagens_pdf.return_value = [] 
    
    mocker.patch('os.path.exists', side_effect=[False, True]) 
    mocker.patch('os.makedirs')
    
    resultado = processar_pdf_empresas_juniores(mock_processor, "http://site.com/doc.pdf")
    
    mock_processor.baixar_pdf_direto.assert_called_once()
    assert len(resultado) == 1

def test_processar_pdf_local_existente(mocker):
    mock_processor = mocker.Mock()
    mock_processor.processar_pdf_paginado.return_value = []
    mock_processor.extrair_imagens_pdf.return_value = []
    
    mocker.patch('os.path.exists', return_value=True)
    
    processar_pdf_empresas_juniores(mock_processor, "/tmp/local.pdf")
    
    mock_processor.baixar_pdf_direto.assert_not_called()

def test_processar_pdf_erro_exception(mocker):
    mock_processor = mocker.Mock()
    mock_processor.baixar_pdf_direto.side_effect = Exception("Erro Download")
    
    mocker.patch('os.path.exists', return_value=False) 
    mocker.patch('os.makedirs')
    
    resultado = processar_pdf_empresas_juniores(mock_processor, "http://url.com")
    
    assert resultado == []

def test_processar_pdf_modo_unico(mocker):
    # Mock do processador
    mock_processor = mocker.Mock()
    mock_processor.processar_pdf_unico.return_value = [{"Nome": "EJ"}]
    mock_processor.extrair_imagens_pdf.return_value = []
    
    mocker.patch('os.path.exists', return_value=True)
    
    mocker.patch('scripts.extrair_empresas_juniores.PROCESSAR_POR_PAGINA', False)
    
    resultado = processar_pdf_empresas_juniores(mock_processor, "local.pdf")
    
    mock_processor.processar_pdf_unico.assert_called_once()
    assert len(resultado) == 1


def test_consolidar_dados_empresas_sucesso(mocker):
    dados = [
        {"Nome": "EJ A", "Cursos": "Eng"},
        {"Nome": "EJ A", "Cursos": "Eng"}, 
        {"Nome": "EJ B", "Cursos": "Comp"}
    ]
    
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)
    mocker.patch("json.dump")
    
    consolidar_dados_empresas(dados, "saida.json")
    
    assert mock_open.called

def test_consolidar_dados_vazio(mocker):
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)
    
    consolidar_dados_empresas([], "saida.json")
    
    assert not mock_open.called

def test_consolidar_dados_erro_escrita(mocker):
    mocker.patch("builtins.open", side_effect=IOError("Erro disco"))
    consolidar_dados_empresas([{"Nome": "A"}], "saida.json")


def test_mostrar_estatisticas_finais(capsys):
    dados = [
        {"Nome": "EJ 1", "Cursos": "A"},
        {"Nome": "EJ 2", "Cursos": "B"}
    ]
    mostrar_estatisticas_finais(dados)
    captured = capsys.readouterr()
    assert "Total de empresas juniores: 2" in captured.out

def test_mostrar_estatisticas_vazio(capsys):
    mostrar_estatisticas_finais([])
    captured = capsys.readouterr()
    assert "Nenhuma empresa" in captured.out


def test_main_fluxo_completo(mocker):
    mocker.patch("scripts.extrair_empresas_juniores.configurar_ambiente", return_value=True)
    
    mock_proc_class = mocker.patch("scripts.extrair_empresas_juniores.PDFProcessorEJs")
    mock_proc_instance = mock_proc_class.return_value
    
    mocker.patch("scripts.extrair_empresas_juniores.processar_pdf_empresas_juniores", return_value=[{"Nome": "EJ"}])
    
    mock_consolidar = mocker.patch("scripts.extrair_empresas_juniores.consolidar_dados_empresas")
    mock_stats = mocker.patch("scripts.extrair_empresas_juniores.mostrar_estatisticas_finais")
    
    main()
    
    mock_consolidar.assert_called_once()
    mock_stats.assert_called_once()

def test_main_falha_config(mocker):
    mocker.patch("scripts.extrair_empresas_juniores.configurar_ambiente", return_value=False)
    mock_proc = mocker.patch("scripts.extrair_empresas_juniores.PDFProcessorEJs")
    
    main()
    
    mock_proc.assert_not_called()

def test_main_sem_dados_extraidos(mocker):
    mocker.patch("scripts.extrair_empresas_juniores.configurar_ambiente", return_value=True)
    mocker.patch("scripts.extrair_empresas_juniores.PDFProcessorEJs")
    mocker.patch("scripts.extrair_empresas_juniores.processar_pdf_empresas_juniores", return_value=[])
    
    mock_consolidar = mocker.patch("scripts.extrair_empresas_juniores.consolidar_dados_empresas")
    
    main()
    

    mock_consolidar.assert_not_called()