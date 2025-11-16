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

    mock_response_html = mocker.Mock()
    mock_response_html.content = HTML_FALSO.encode('utf-8') # Converte string para bytes
    mock_response_html.raise_for_status = mocker.Mock() # Finge que foi 200 OK

    mock_requests_get = mocker.patch('scripts.labs_pdf.requests.get')
    mock_requests_get.return_value = mock_response_html

    mock_link_encontrado = {'href': '/caminho/relativo/Portfolio_Infraestrutura_UnB.pdf'}
    mock_soup_instance = mocker.Mock()
    mock_soup_instance.find_all.return_value = [mock_link_encontrado]
    mocker.patch('scripts.labs_pdf.BeautifulSoup', return_value=mock_soup_instance)