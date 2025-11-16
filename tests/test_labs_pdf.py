import pytest
import os
import scripts.labs_pdf
from bs4 import BeautifulSoup


def test_labs_pdf_baixa_o_arquivo_com_sucesso(mocker):

    HTML_FALSO = """
    <html>
      <body>
        <a href="http://site-errado.com/outro.pdf">Link irrelevante</a>
        <a href="/caminho/relativo/Portfolio_Infraestrutura_UnB.pdf">Nosso PDF</a>
      </body>
    </html>
    """
    DADOS_PDF_FALSOS = b"%PDF-1.4 fake pdf content" # b'' significa bytes

    # 1.1: Mock do requests.get (1ª chamada: HTML)
    mock_response_html = mocker.Mock()
    mock_response_html.content = HTML_FALSO.encode('utf-8')
    mock_response_html.raise_for_status = mocker.Mock()

    # 1.2: Mock do requests.get (2ª chamada: PDF)
    mock_response_pdf = mocker.Mock()
    mock_response_pdf.iter_content.return_value = [DADOS_PDF_FALSOS]
    mock_response_pdf.raise_for_status = mocker.Mock()

    # 1.3: Configura o 'requests.get' para retornar as duas respostas em ordem
    mock_requests_get = mocker.patch('scripts.labs_pdf.requests.get')
    mock_requests_get.side_effect = [mock_response_html, mock_response_pdf]

    # 1.4: Mock do BeautifulSoup
    mock_link_encontrado = {'href': '/caminho/relativo/Portfolio_Infraestrutura_UnB.pdf'}
    mock_soup_instance = mocker.Mock()
    mock_soup_instance.find_all.return_value = [mock_link_encontrado]
    mocker.patch('scripts.labs_pdf.BeautifulSoup', return_value=mock_soup_instance)

    # 1.5: Mock do Sistema de Arquivos (para não criar pastas ou arquivos)
    mocker.patch('scripts.labs_pdf.os.makedirs')
    mock_open = mocker.patch('builtins.open', mocker.mock_open())