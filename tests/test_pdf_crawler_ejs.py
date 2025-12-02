import pytest
import os
import requests
from unittest.mock import Mock, patch, mock_open, ANY
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from scripts.pdf_crawler_ejs import encontrar_pdf_empresas_juniores

def test_pdf_crawler_ejs_baixa_o_arquivo_com_sucesso(mocker):
    """Testa o fluxo de sucesso completo"""
    mock_resp_html = Mock()
    mock_resp_html.content = b'<html><a href="ej.pdf">EJ Portfolio</a></html>'
    mock_resp_html.raise_for_status = Mock()
    
    mock_resp_pdf = Mock()
    mock_resp_pdf.iter_content.return_value = [b"pdf data"]
    mock_resp_pdf.raise_for_status = Mock()
    
    mock_requests = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_requests.side_effect = [mock_resp_html, mock_resp_pdf]
    
    mock_makedirs = mocker.patch('scripts.pdf_crawler_ejs.os.makedirs')
    mock_open_file = mocker.patch('builtins.open', mocker.mock_open())
    
    resultado = encontrar_pdf_empresas_juniores("http://teste.com")
    
    assert resultado is not None
    assert "portfolio_empresas_juniores.pdf" in resultado
    mock_makedirs.assert_called()
    mock_open_file().write.assert_called_with(b"pdf data")

def test_pdf_crawler_ejs_sem_pdfs_encontrados(mocker):
    """Testa quando não há links PDF na página"""
    mock_resp_html = Mock()
    mock_resp_html.content = b'<html><a href="doc.txt">Doc</a></html>'
    
    mocker.patch('scripts.pdf_crawler_ejs.requests.get', return_value=mock_resp_html)
    
    mock_print = mocker.patch('builtins.print')
        
    resultado = encontrar_pdf_empresas_juniores("http://teste.com")
        
    assert resultado is None
    assert any("Nenhum PDF" in str(call) for call in mock_print.mock_calls)

def test_pdf_crawler_ejs_falha_timeout(mocker):
    """Testa exceção de Timeout"""
    mocker.patch('scripts.pdf_crawler_ejs.requests.get', side_effect=requests.exceptions.Timeout)
    
    mock_print = mocker.patch('builtins.print')
    
    resultado = encontrar_pdf_empresas_juniores("http://teste.com")
        
    assert resultado is None
    assert any("timeout" in str(call) for call in mock_print.mock_calls)

def test_pdf_crawler_ejs_falha_conexao(mocker):
    """Testa exceção de ConnectionError"""
    mocker.patch('scripts.pdf_crawler_ejs.requests.get', side_effect=requests.exceptions.ConnectionError)
    
    mock_print = mocker.patch('builtins.print')
    
    resultado = encontrar_pdf_empresas_juniores("http://teste.com")
        
    assert resultado is None
    assert any("Não foi possível conectar" in str(call) for call in mock_print.mock_calls)

def test_pdf_crawler_ejs_falha_http(mocker):
    """Testa exceção de HTTPError (ex: 404)"""
    mocker.patch('scripts.pdf_crawler_ejs.requests.get', side_effect=requests.exceptions.HTTPError("404"))
    
    mock_print = mocker.patch('builtins.print')
    
    resultado = encontrar_pdf_empresas_juniores("http://teste.com")
        
    assert resultado is None
    assert any("ERRO HTTP" in str(call) for call in mock_print.mock_calls)

def test_pdf_crawler_ejs_falha_generica(mocker):
    """Testa exceção genérica RequestException"""
    mocker.patch('scripts.pdf_crawler_ejs.requests.get', side_effect=requests.exceptions.RequestException("Erro Geral"))
    
    mock_print = mocker.patch('builtins.print')
    
    resultado = encontrar_pdf_empresas_juniores("http://teste.com")
        
    assert resultado is None
    assert any("Erro ao acessar a página" in str(call) for call in mock_print.mock_calls)

def test_pdf_crawler_filtro_links(mocker):
    """Testa a lógica específica de filtragem de links"""
    html = """
    <html>
        <a href="certo.pdf">EJ Portfolio</a>  <a href="errado.pdf">Relatório</a>    <a href="outro.doc">EJ Doc</a>        </html>
    """
    mock_resp = Mock()
    mock_resp.content = html.encode('utf-8')
    
    mock_resp_pdf = Mock()
    mock_resp_pdf.iter_content.return_value = []
    
    mock_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_get.side_effect = [mock_resp, mock_resp_pdf]
    
    mocker.patch('scripts.pdf_crawler_ejs.os.makedirs')
    mocker.patch('builtins.open', mocker.mock_open())
    
    encontrar_pdf_empresas_juniores("http://teste.com")
    
    args, _ = mock_get.call_args
    assert "certo.pdf" in args[0]