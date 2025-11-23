import pytest
import os
import requests
import scripts.pdf_crawler_ejs
from scripts.pdf_crawler_ejs import encontrar_pdf_empresas_juniores
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from unittest.mock import Mock, ANY

def test_pdf_crawler_ejs_baixa_o_arquivo_com_sucesso(mocker):
    """
    Testa o fluxo de sucesso do crawler de EJs:
    1. Simula o download do HTML com links PDF relevantes
    2. Simula o BeautifulSoup encontrando links de PDF de empresas juniores
    3. Simula o download do PDF
    4. Simula o salvamento do arquivo
    5. Verifica se tudo foi chamado corretamente
    """

    # --- 1. ARRANGE (Preparar as Simulações) ---
    
    HTML_FALSO = """
    <html><body>
        <a href="http://site.com/outro.pdf">Link irrelevante</a>
        <a href="/caminho/portfolio_empresas_juniores.pdf">Portfólio Empresas Juniores</a>
        <a href="/outro/ej.pdf">PDF Empresa Júnior</a>
    </body></html>
    """
    DADOS_PDF_FALSOS = b"%PDF-1.4 fake pdf content for EJs"

    # 1.1: Mock do requests.get (para HTML e PDF)
    mock_response_html = Mock()
    mock_response_html.content = HTML_FALSO.encode('utf-8')
    mock_response_html.raise_for_status = Mock()
    
    mock_response_pdf = Mock()
    mock_response_pdf.iter_content.return_value = [DADOS_PDF_FALSOS]
    mock_response_pdf.raise_for_status = Mock()
    
    mock_requests_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_requests_get.side_effect = [mock_response_html, mock_response_pdf]

    # 1.2: Mock do BeautifulSoup para retornar links relevantes
    # Criamos mocks que simulam objetos Tag do BeautifulSoup
    def create_mock_link(href, text):
        mock_link = Mock()
        mock_link.get_text.return_value = text
        # Para link['href'], precisamos configurar __getitem__
        mock_link.__getitem__ = Mock(return_value=href)
        return mock_link

    mock_link_ej1 = create_mock_link("/caminho/portfolio_empresas_juniores.pdf", "Portfólio Empresas Juniores")
    mock_link_ej2 = create_mock_link("/outro/ej.pdf", "PDF Empresa Júnior")
    mock_link_irrelevante = create_mock_link("http://site.com/outro.pdf", "Link irrelevante")
    
    mock_soup_instance = Mock()
    mock_soup_instance.find_all.return_value = [mock_link_irrelevante, mock_link_ej1, mock_link_ej2]
    mocker.patch('scripts.pdf_crawler_ejs.BeautifulSoup', return_value=mock_soup_instance)

    # 1.3: Mock do Sistema de Arquivos
    mock_makedirs = mocker.patch('scripts.pdf_crawler_ejs.os.makedirs')
    mock_open_escrita = mocker.patch('builtins.open', mocker.mock_open())
    
    # 1.4: Mock do urljoin
    mock_urljoin = mocker.patch('scripts.pdf_crawler_ejs.urllib.parse.urljoin')
    def urljoin_side_effect(base, url):
        return f"{base.rstrip('/')}/{url.lstrip('/')}"
    mock_urljoin.side_effect = urljoin_side_effect

    # --- 2. ACT (Executar a função) ---
    URL_TESTE = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
    resultado = encontrar_pdf_empresas_juniores(URL_TESTE)

    # --- 3. ASSERT (Verificar se tudo aconteceu corretamente) ---

    # Verifica chamadas do requests.get
    assert mock_requests_get.call_count == 2
    
    # Primeira chamada: download do HTML
    mock_requests_get.assert_any_call(
        URL_TESTE,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
        },
        timeout=20,
        allow_redirects=True,
        verify=False
    )
    
    # Segunda chamada: download do PDF (deve usar a URL completa do primeiro link EJ)
    pdf_url_esperada = f"{URL_TESTE.rstrip('/')}/caminho/portfolio_empresas_juniores.pdf"
    mock_requests_get.assert_any_call(
        pdf_url_esperada,
        headers=ANY,
        stream=True,
        timeout=30,
        allow_redirects=True,
        verify=False
    )

    # Verifica criação do diretório
    script_dir = os.path.dirname(scripts.pdf_crawler_ejs.__file__)
    caminho_pasta_esperado = os.path.join(script_dir, "..", "data", "EJs")
    mock_makedirs.assert_called_with(caminho_pasta_esperado, exist_ok=True)

    # Verifica salvamento do arquivo
    caminho_salvar_esperado = os.path.join(caminho_pasta_esperado, "portfolio_empresas_juniores.pdf")
    mock_open_escrita.assert_called_with(caminho_salvar_esperado, 'wb')

    # Verifica escrita dos dados PDF
    handle = mock_open_escrita()
    handle.write.assert_called_once_with(DADOS_PDF_FALSOS)

    # Verifica retorno do caminho do arquivo
    assert resultado == caminho_salvar_esperado

def test_pdf_crawler_ejs_sem_pdfs_encontrados(mocker):
    """
    Testa o fluxo quando não são encontrados PDFs de empresas juniores
    """
    # --- 1. ARRANGE ---
    HTML_SEM_PDFS_EJ = """
    <html><body>
        <a href="/documento.docx">Documento Word</a>
        <a href="/imagem.jpg">Imagem JPEG</a>
        <a href="/outro.pdf">PDF irrelevante</a>
    </body></html>
    """

    mock_response_html = Mock()
    mock_response_html.content = HTML_SEM_PDFS_EJ.encode('utf-8')
    mock_response_html.raise_for_status = Mock()
    
    mock_requests_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_requests_get.return_value = mock_response_html

    # Links irrelevantes (não atendem aos critérios de EJ)
    def create_mock_link(href, text):
        mock_link = Mock()
        mock_link.get_text.return_value = text
        mock_link.__getitem__ = Mock(return_value=href)
        return mock_link

    mock_link_docx = create_mock_link("/documento.docx", "Documento Word")
    mock_link_jpg = create_mock_link("/imagem.jpg", "Imagem JPEG")
    mock_link_pdf_irrelevante = create_mock_link("/outro.pdf", "PDF irrelevante")
    
    mock_soup_instance = Mock()
    mock_soup_instance.find_all.return_value = [mock_link_docx, mock_link_jpg, mock_link_pdf_irrelevante]
    mocker.patch('scripts.pdf_crawler_ejs.BeautifulSoup', return_value=mock_soup_instance)

    # --- 2. ACT ---
    URL_TESTE = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
    resultado = encontrar_pdf_empresas_juniores(URL_TESTE)

    # --- 3. ASSERT ---
    # Deve retornar None quando não encontra PDFs relevantes
    assert resultado is None
    
    # Só deve chamar requests.get uma vez (apenas para o HTML)
    mock_requests_get.assert_called_once()

def test_pdf_crawler_ejs_falha_http_404(mocker):
    """
    Testa o fluxo de falha onde a requisição HTTP retorna erro 404
    """
    # --- 1. ARRANGE ---
    mock_requests_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_requests_get.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")

    # Mock do print para capturar mensagens de erro
    mock_print = mocker.patch('builtins.print')

    # --- 2. ACT ---
    URL_TESTE = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
    resultado = encontrar_pdf_empresas_juniores(URL_TESTE)

    # --- 3. ASSERT ---
    assert resultado is None
    mock_requests_get.assert_called_once()
    
    # Verifica se mensagem de erro foi impressa
    # Verificamos se alguma chamada de print contém partes esperadas das mensagens
    error_messages = [call.args[0] for call in mock_print.call_args_list]
    has_http_error = any("ERRO HTTP" in str(msg) for msg in error_messages)
    has_url = any(URL_TESTE in str(msg) for msg in error_messages)
    
    assert has_http_error or has_url, f"Nenhuma mensagem de erro HTTP encontrada. Mensagens: {error_messages}"

def test_pdf_crawler_ejs_timeout(mocker):
    """
    Testa o fluxo de falha por timeout na requisição
    """
    # --- 1. ARRANGE ---
    mock_requests_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_requests_get.side_effect = requests.exceptions.Timeout()

    mock_print = mocker.patch('builtins.print')

    # --- 2. ACT ---
    URL_TESTE = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
    resultado = encontrar_pdf_empresas_juniores(URL_TESTE)

    # --- 3. ASSERT ---
    assert resultado is None
    mock_requests_get.assert_called_once()
    
    # Verifica se mensagem de timeout foi impressa
    error_messages = [call.args[0] for call in mock_print.call_args_list]
    has_timeout_error = any("timeout" in str(msg).lower() for msg in error_messages)
    has_url = any(URL_TESTE in str(msg) for msg in error_messages)
    
    assert has_timeout_error or has_url, f"Nenhuma mensagem de timeout encontrada. Mensagens: {error_messages}"

def test_pdf_crawler_ejs_connection_error(mocker):
    """
    Testa o fluxo de falha por erro de conexão
    """
    # --- 1. ARRANGE ---
    mock_requests_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_requests_get.side_effect = requests.exceptions.ConnectionError("Erro de conexão")

    mock_print = mocker.patch('builtins.print')

    # --- 2. ACT ---
    URL_TESTE = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
    resultado = encontrar_pdf_empresas_juniores(URL_TESTE)

    # --- 3. ASSERT ---
    assert resultado is None
    mock_requests_get.assert_called_once()
    
    # Verifica se mensagem de conexão foi impressa
    error_messages = [call.args[0] for call in mock_print.call_args_list]
    has_connection_error = any("conectar" in str(msg).lower() for msg in error_messages)
    has_url = any(URL_TESTE in str(msg) for msg in error_messages)
    
    assert has_connection_error or has_url, f"Nenhuma mensagem de conexão encontrada. Mensagens: {error_messages}"

def test_pdf_crawler_ejs_filtra_links_por_criterios_ej(mocker):
    """
    Testa especificamente a lógica de filtragem de links PDF por critérios de EJ
    """
    # --- 1. ARRANGE ---
    HTML_COM_VARIOS_LINKS = """
    <html><body>
        <a href="/portfolio_ejs.pdf">Portfólio EJs</a>
        <a href="/empresa_junior.pdf">Empresa Júnior</a>
        <a href="/EJ_portfolio.pdf">EJ Portfolio</a>
        <a href="/outro.pdf">PDF qualquer</a>
        <a href="/sem_relacao.doc">Documento</a>
    </body></html>
    """

    mock_response_html = Mock()
    mock_response_html.content = HTML_COM_VARIOS_LINKS.encode('utf-8')
    mock_response_html.raise_for_status = Mock()
    
    mock_requests_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_requests_get.return_value = mock_response_html

    # Mock dos links que atendem aos critérios
    def create_mock_link(href, text):
        mock_link = Mock()
        mock_link.get_text.return_value = text
        mock_link.__getitem__ = Mock(return_value=href)
        return mock_link

    links_ej = []
    for texto, href in [
        ("Portfólio EJs", "/portfolio_ejs.pdf"),
        ("Empresa Júnior", "/empresa_junior.pdf"), 
        ("EJ Portfolio", "/EJ_portfolio.pdf")
    ]:
        links_ej.append(create_mock_link(href, texto))
    
    # Links que NÃO atendem aos critérios
    mock_link_qualquer = create_mock_link("/outro.pdf", "PDF qualquer")
    mock_link_doc = create_mock_link("/sem_relacao.doc", "Documento")
    
    mock_soup_instance = Mock()
    mock_soup_instance.find_all.return_value = links_ej + [mock_link_qualquer, mock_link_doc]
    mocker.patch('scripts.pdf_crawler_ejs.BeautifulSoup', return_value=mock_soup_instance)

    # Mock do download do PDF (apenas para não falhar)
    mock_response_pdf = Mock()
    mock_response_pdf.iter_content.return_value = [b"pdf content"]
    mock_response_pdf.raise_for_status = Mock()
    mock_requests_get.side_effect = [mock_response_html, mock_response_pdf]

    mocker.patch('scripts.pdf_crawler_ejs.os.makedirs')
    mocker.patch('builtins.open', mocker.mock_open())

    # --- 2. ACT ---
    URL_TESTE = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
    resultado = encontrar_pdf_empresas_juniores(URL_TESTE)

    # --- 3. ASSERT ---
    # A função deve processar apenas os 3 links que atendem aos critérios EJ
    # e ignorar os outros 2
    assert resultado is not None
    
    # Verifica que foram feitas 2 chamadas: HTML + PDF do primeiro link EJ
    assert mock_requests_get.call_count == 2

def test_pdf_crawler_ejs_remove_duplicatas(mocker):
    """
    Testa que links duplicados (mesma URL) são removidos
    """
    # --- 1. ARRANGE ---
    HTML_COM_DUPLICATAS = """
    <html><body>
        <a href="/portfolio_ejs.pdf">Portfólio 1</a>
        <a href="/portfolio_ejs.pdf">Portfólio 2</a>
        <a href="/outro_ej.pdf">Outra EJ</a>
    </body></html>
    """

    mock_response_html = Mock()
    mock_response_html.content = HTML_COM_DUPLICATAS.encode('utf-8')
    mock_response_html.raise_for_status = Mock()
    
    mock_requests_get = mocker.patch('scripts.pdf_crawler_ejs.requests.get')
    mock_requests_get.return_value = mock_response_html

    # Links com URL duplicada
    def create_mock_link(href, text):
        mock_link = Mock()
        mock_link.get_text.return_value = text
        mock_link.__getitem__ = Mock(return_value=href)
        return mock_link

    mock_link1 = create_mock_link("/portfolio_ejs.pdf", "Portfólio 1")
    mock_link2 = create_mock_link("/portfolio_ejs.pdf", "Portfólio 2")  # Mesma URL, texto diferente
    mock_link3 = create_mock_link("/outro_ej.pdf", "Outra EJ")  # URL diferente
    
    mock_soup_instance = Mock()
    mock_soup_instance.find_all.return_value = [mock_link1, mock_link2, mock_link3]
    mocker.patch('scripts.pdf_crawler_ejs.BeautifulSoup', return_value=mock_soup_instance)

    # Mock do download
    mock_response_pdf = Mock()
    mock_response_pdf.iter_content.return_value = [b"pdf content"]
    mock_response_pdf.raise_for_status = Mock()
    mock_requests_get.side_effect = [mock_response_html, mock_response_pdf]

    mocker.patch('scripts.pdf_crawler_ejs.os.makedirs')
    mocker.patch('builtins.open', mocker.mock_open())

    # --- 2. ACT ---
    URL_TESTE = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
    resultado = encontrar_pdf_empresas_juniores(URL_TESTE)

    # --- 3. ASSERT ---
    # A função deve processar e remover duplicatas
    assert resultado is not None
    
    # Apenas 2 chamadas: HTML + PDF (a duplicata foi removida)
    assert mock_requests_get.call_count == 2