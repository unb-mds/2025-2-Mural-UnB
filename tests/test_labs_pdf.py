import pytest
import os
import requests 

# Importa o módulo (para mockar) e a função (para chamar)
import scripts.labs_pdf
from scripts.labs_pdf import main # <-- CORREÇÃO: Garante que 'main' está importado
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def test_labs_pdf_baixa_o_arquivo_com_sucesso(mocker):
    """
    Testa o fluxo de sucesso:
    1. Simula o download do HTML
    2. Simula o BeautifulSoup encontrando o link
    3. Simula o download do PDF
    4. Simula o salvamento do arquivo
    5. Verifica se tudo foi chamado corretamente.
    """

    # --- 1. ARRANGE (Preparar as "Mentiras"/Simulações) ---
    
    HTML_FALSO = """
    <html><body>
        <a href="http://site-errado.com/outro.pdf">Link irrelevante</a>
        <a href="/caminho/relativo/Portfolio_Infraestrutura_UnB.pdf">Nosso PDF</a>
    </body></html>
    """
    DADOS_PDF_FALSOS = b"%PDF-1.4 fake pdf content"

    # 1.1: Mock do requests.get (para HTML e PDF)
    mock_response_html = mocker.Mock()
    mock_response_html.content = HTML_FALSO.encode('utf-8')
    mock_response_html.raise_for_status = mocker.Mock()
    
    mock_response_pdf = mocker.Mock()
    mock_response_pdf.iter_content.return_value = [DADOS_PDF_FALSOS]
    mock_response_pdf.raise_for_status = mocker.Mock()
    
    mock_requests_get = mocker.patch('scripts.labs_pdf.requests.get')
    mock_requests_get.side_effect = [mock_response_html, mock_response_pdf]

    # 1.2: Mock do BeautifulSoup 
    mock_link_tag = mocker.Mock()
    mock_link_tag.get_text.return_value = "Portfolio Falso"
    
    # CORREÇÃO: Configura o .get() para retornar o link
    mock_link_tag.get.return_value = "/caminho/relativo/Portfolio_Infraestrutura_UnB.pdf"
    
    mock_soup_instance = mocker.Mock()
    mock_soup_instance.find_all.return_value = [mock_link_tag]
    mocker.patch('scripts.labs_pdf.BeautifulSoup', return_value=mock_soup_instance)

    # 1.3: Mock do Sistema de Arquivos
    mock_makedirs = mocker.patch('scripts.labs_pdf.os.makedirs')
    mock_open_escrita = mocker.patch('builtins.open', mocker.mock_open()) 
    
    # 1.4: Mock do urljoin
    mock_urljoin = mocker.patch('scripts.labs_pdf.urllib.parse.urljoin')
    mock_urljoin.return_value = "http://pesquisa.unb.br/caminho/relativo/Portfolio_Infraestrutura_UnB.pdf"
    
    main() # <--- ACT

    # --- 3. ASSERT (Verificar se tudo aconteceu) ---

    assert mock_requests_get.call_count == 2
    mock_requests_get.assert_called_with(
        "http://pesquisa.unb.br/caminho/relativo/Portfolio_Infraestrutura_UnB.pdf", 
        stream=True, 
        timeout=30
    )

    script_dir = os.path.dirname(scripts.labs_pdf.__file__)
    caminho_pasta_esperado = os.path.join(script_dir, "..", "data", "Labs")
    mock_makedirs.assert_called_with(caminho_pasta_esperado, exist_ok=True)

    caminho_salvar_esperado = os.path.join(caminho_pasta_esperado, "Portfolio_Infraestrutura_UnB.pdf")
    mock_open_escrita.assert_called_with(caminho_salvar_esperado, 'wb')

    handle = mock_open_escrita()
    handle.write.assert_called_once_with(DADOS_PDF_FALSOS)

def test_labs_pdf_falha_http_404(mocker):
    """
    Testa o fluxo de falha onde a primeira chamada (baixar HTML) 
    retorna um erro HTTP 404.
    """
    # --- 1. ARRANGE ---
    mock_requests_get = mocker.patch('scripts.labs_pdf.requests.get')
    mock_requests_get.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")

    mock_exit = mocker.patch('scripts.labs_pdf.exit')

    # --- 2. ACT ---
    main() 

    # --- 3. ASSERT ---
    mock_requests_get.assert_called_once()
    mock_exit.assert_called_once_with(1)