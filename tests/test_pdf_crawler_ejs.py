"""
Testes unitários para pdf_crawler_ejs.py
"""
import os
import sys
import pytest
import requests
from unittest.mock import patch, MagicMock, mock_open

# Adiciona o diretório scripts ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_encontrar_pdf_empresas_juniores_sucesso(mocker):
    """Testa o fluxo de sucesso do crawler"""
    # Mock das dependências
    mock_requests_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_beautifulsoup = mocker.patch('scripts.pdf_crawler_ejs.BeautifulSoup')
    mock_urljoin = mocker.patch('scripts.pdf_crawler_ejs.urllib.parse.urljoin')
    mock_os_makedirs = mocker.patch('scripts.pdf_crawler_ejs.os.makedirs')
    mock_open_file = mocker.patch('builtins.open', mock_open())
    
    # Configurar mocks
    mock_response_html = MagicMock()
    mock_response_html.content = b'<html><a href="portfolio.pdf">Empresa Junior PDF</a></html>'
    mock_response_html.raise_for_status = MagicMock()
    
    mock_response_pdf = MagicMock()
    mock_response_pdf.iter_content.return_value = [b'%PDF-1.4 fake content']
    mock_response_pdf.raise_for_status = MagicMock()
    
    mock_requests_get.side_effect = [mock_response_html, mock_response_pdf]
    
    mock_soup_instance = MagicMock()
    mock_link = MagicMock()
    mock_link.get_text.return_value = 'Empresa Junior PDF'
    mock_link.__getitem__.return_value = 'portfolio.pdf'
    mock_soup_instance.find_all.return_value = [mock_link]
    mock_beautifulsoup.return_value = mock_soup_instance
    
    mock_urljoin.return_value = 'https://unb.br/portfolio.pdf'
    
    # Importar e executar
    from scripts.pdf_crawler_ejs import encontrar_pdf_empresas_juniores
    
    url_teste = "https://unb.br/empresas-juniores"
    resultado = encontrar_pdf_empresas_juniores(url_teste)
    
    # Verificações
    assert resultado is not None
    assert "portfolio_empresas_juniores.pdf" in resultado
    mock_requests_get.assert_called()
    mock_os_makedirs.assert_called_once()

def test_encontrar_pdf_empresas_juniores_timeout():
    """Testa comportamento em caso de timeout"""
    with patch('scripts.pdf_crawler_ejs.requests.get') as mock_requests_get:
        
        mock_requests_get.side_effect = requests.exceptions.Timeout("Timeout")
        
        from scripts.pdf_crawler_ejs import encontrar_pdf_empresas_juniores
        
        resultado = encontrar_pdf_empresas_juniores("https://unb.br/test")
        
        assert resultado is None

def test_encontrar_pdf_empresas_juniores_sem_pdfs(mocker):
    """Testa quando não encontra PDFs relevantes"""
    mock_requests_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_beautifulsoup = mocker.patch('scripts.pdf_crawler_ejs.BeautifulSoup')
    
    mock_response = MagicMock()
    mock_response.content = b'<html><a href="image.jpg">Imagem</a></html>'
    mock_response.raise_for_status = MagicMock()
    mock_requests_get.return_value = mock_response
    
    mock_soup_instance = MagicMock()
    mock_soup_instance.find_all.return_value = []  # Nenhum link PDF
    mock_beautifulsoup.return_value = mock_soup_instance
    
    from scripts.pdf_crawler_ejs import encontrar_pdf_empresas_juniores
    
    resultado = encontrar_pdf_empresas_juniores("https://unb.br/test")
    
    assert resultado is None

def test_encontrar_pdf_empresas_juniores_http_error():
    """Testa comportamento em caso de erro HTTP"""
    with patch('scripts.pdf_crawler_ejs.requests.get') as mock_requests_get:
        
        mock_requests_get.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        from scripts.pdf_crawler_ejs import encontrar_pdf_empresas_juniores
        
        resultado = encontrar_pdf_empresas_juniores("https://unb.br/invalid")
        
        assert resultado is None

def test_encontrar_pdf_empresas_juniores_connection_error():
    """Testa comportamento em caso de erro de conexão"""
    with patch('scripts.pdf_crawler_ejs.requests.get') as mock_requests_get:
       
        mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        from scripts.pdf_crawler_ejs import encontrar_pdf_empresas_juniores
        
        resultado = encontrar_pdf_empresas_juniores("https://unb.br/invalid")
        
        assert resultado is None

def test_encontrar_pdf_empresas_juniores_request_exception():
    """Testa comportamento em caso de exceção genérica de requests"""
    with patch('scripts.pdf_crawler_ejs.requests.get') as mock_requests_get:
        
        mock_requests_get.side_effect = requests.exceptions.RequestException("Generic error")
        
        from scripts.pdf_crawler_ejs import encontrar_pdf_empresas_juniores
        
        resultado = encontrar_pdf_empresas_juniores("https://unb.br/invalid")
        
        assert resultado is None