import pytest
import os
import random
import csv
import textwrap
from unittest.mock import MagicMock

from scripts.extrair_labs_fga import (
    extrair_palavra_chave,
    categorizar_lab,
    limpar_texto,
    juntar_palavras_hifenizadas,
    encontrar_imagem_para_lab,
    filtrar_labs_fga,
    extrair_laboratorios_fga_pdf,
    baixar_imagem,
    main # Importando a main para cobertura total
)

# --- Testes Unitários de Helpers ---

def test_extrair_palavra_chave_sucesso():
    assert extrair_palavra_chave("Laboratório de Robótica") == "robotica"

def test_extrair_palavra_chave_sem_chave():
    assert extrair_palavra_chave("Laboratório de Pesquisa da UnB") == "pesquisa"

def test_extrair_palavra_chave_erro_interno(mocker):
    mocker.patch("scripts.extrair_labs_fga.unidecode", side_effect=Exception("Boom"))
    assert extrair_palavra_chave("Qualquer coisa") == "pesquisa"

def test_categorizar_lab_todos_tipos():
    assert categorizar_lab("IA Lab") == "software"
    assert categorizar_lab("Laboratório de Circuitos") == "eletronica"
    assert categorizar_lab("Mecânica Lab") == "mecanica_materiais"
    assert categorizar_lab("Lab X") == "default"

def test_categorizar_lab_erro(mocker):
    mocker.patch("scripts.extrair_labs_fga.unidecode", side_effect=Exception("Boom"))
    assert categorizar_lab("Lab") == "default"

def test_limpar_texto():
    assert limpar_texto("Texto\u202fcom\xa0sujeira") == "Texto com sujeira"
    assert limpar_texto(None) is None

def test_juntar_palavras_hifenizadas():
    assert juntar_palavras_hifenizadas("separa-\ndo") == "separado"
    assert juntar_palavras_hifenizadas(None) is None

# --- Testes de Baixar Imagem ---

def test_baixar_imagem_sucesso(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "image/jpeg"}
    mock_response.iter_content.return_value = [b"data"]
    
    mocker.patch("scripts.extrair_labs_fga.requests.get", return_value=mock_response)
    mocker.patch("builtins.open", mocker.mock_open())
    mocker.patch("os.makedirs")

    assert baixar_imagem("http://url.com/img.jpg", "/path/img.jpg") is True

def test_baixar_imagem_falhas(mocker):
    import requests
    # 1. Não é imagem
    mock_resp_bad = mocker.Mock()
    mock_resp_bad.status_code = 200
    mock_resp_bad.headers = {"content-type": "text/html"}
    mocker.patch("scripts.extrair_labs_fga.requests.get", return_value=mock_resp_bad)
    assert baixar_imagem("http://url.com/fake.jpg", "/p") is False
    
    # 2. Timeout
    mocker.patch("scripts.extrair_labs_fga.requests.get", side_effect=requests.exceptions.Timeout)
    assert baixar_imagem("http://url.com/to.jpg", "/p") is False

    # 3. Erro Genérico
    mocker.patch("scripts.extrair_labs_fga.requests.get", side_effect=Exception("Erro"))
    assert baixar_imagem("http://url.com/err.jpg", "/p") is False

# --- Testes de Encontrar Imagem ---

def test_encontrar_imagem_para_lab_fluxo_sucesso(mocker):
    mock_ddgs = mocker.patch('scripts.extrair_labs_fga.DDGS')
    mock_ddgs.return_value.__enter__.return_value.text.return_value = [{'href': 'http://unb.br/lab', 'title': 'Lab'}]
    
    mock_resp = mocker.Mock()
    mock_resp.content = b'<html><meta property="og:image" content="img.jpg"></html>'
    mocker.patch('scripts.extrair_labs_fga.requests.get', return_value=mock_resp)
    mocker.patch('scripts.extrair_labs_fga.baixar_imagem', return_value=True)
    mocker.patch('scripts.extrair_labs_fga.urljoin', side_effect=lambda a, b: b)

    path = encontrar_imagem_para_lab("Lab Teste", "/tmp")
    assert path is not None

def test_encontrar_imagem_filtros_avancados(mocker):
    resultados_busca = [
        {'href': 'http://facebook.com/lab', 'title': 'FB'}, 
        {'href': 'http://outro.com/lab', 'title': 'Lab Externo'},
    ]
    mock_ddgs = mocker.patch('scripts.extrair_labs_fga.DDGS')
    mock_ddgs.return_value.__enter__.return_value.text.return_value = resultados_busca

    html_content = """
    <html>
        <meta property="og:image" content="bad.svg">
        <img id="logo" src="logo.png" width="10" height="10">
        <div class="banner">
            <img src="banner.jpg" width="500" height="300">
        </div>
    </html>
    """
    mock_resp = mocker.Mock()
    mock_resp.content = html_content.encode('utf-8')
    mocker.patch('scripts.extrair_labs_fga.requests.get', return_value=mock_resp)
    
    mock_baixar = mocker.patch('scripts.extrair_labs_fga.baixar_imagem', return_value=True)
    mocker.patch('scripts.extrair_labs_fga.urljoin', side_effect=lambda base, url: url)

    caminho = encontrar_imagem_para_lab("Lab Teste", "/tmp")
    
    assert caminho is not None
    mock_baixar.assert_called_with("banner.jpg", mocker.ANY)

def test_encontrar_imagem_sem_resultados(mocker):
    mock_ddgs = mocker.patch('scripts.extrair_labs_fga.DDGS')
    mock_ddgs.return_value.__enter__.return_value.text.return_value = []
    assert encontrar_imagem_para_lab("Lab", "/tmp") is None

# --- Testes de Parsing de PDF (A parte mais complexa) ---

def test_extrair_laboratorios_fga_pdf_parsing_complexo(mocker):
    # Dedent remove a indentação comum, simulando texto real alinhado à esquerda
    texto_sujo = textwrap.dedent("""
        1.2.3. Seção Irrelevante
        Texto aleatório.
        ____________________

        10. Lab FGA Real
        COORDENADOR: Prof. A (ID Lattes: 123)
        CONTATO: a@unb.br
        DESCRIÇÃO: Lab de software na FGA.
        CLASSIFICAÇÃO: Pesquisa.
        UNIVERSIDADE DE BRASÍLIA
        
        11.
        Lab Com Nome na Outra Linha
        COORDENADORES: Prof. B
        DESCRICAO: pesqui-
        sa de ponta.
        IV - INFRAESTRUTURA
        
        12. Lab Ignorado
        DESCRIÇÃO: Não tem a sigla mágica na descrição nem no nome.
    """)
    
    mock_doc = mocker.MagicMock()
    mock_page = mocker.Mock()
    mock_page.get_text.return_value = texto_sujo
    mock_doc.__len__.return_value = 1
    mock_doc.__getitem__.return_value = mock_page
    mocker.patch("fitz.open", return_value=mock_doc)

    # Força pagina_inicial=1
    labs = extrair_laboratorios_fga_pdf("dummy.pdf", pagina_inicial=1)

    assert len(labs) >= 2
    
    lab10 = next(l for l in labs if "Lab FGA Real" in l['nome'])
    assert "Prof. A" in lab10['coordenador']
    assert "Pesquisa" not in lab10['descricao']

    lab11 = next(l for l in labs if "Lab Com Nome na Outra Linha" in l['nome'])
    assert "pesquisa de ponta" in lab11['descricao']

# --- Teste de Integração ---

def test_filtrar_labs_fga_integration(mocker):
    mocker.patch('scripts.extrair_labs_fga.extrair_laboratorios_fga_pdf', return_value=[
        {'nome': 'Lab 1', 'descricao': 'FGA', 'coordenador': 'A', 'contato': 'B'},
        {'nome': 'Lab 1', 'descricao': 'FGA Duplicado', 'coordenador': 'A', 'contato': 'B'},
        {'nome': 'Lab 2', 'descricao': 'Outra coisa'}
    ])
    
    mocker.patch('scripts.extrair_labs_fga.encontrar_imagem_para_lab', side_effect=["img1.jpg", None])
    mocker.patch('scripts.extrair_labs_fga.random.randint', return_value=1)
    
    mock_file = mocker.mock_open()
    mocker.patch('builtins.open', mock_file)
    mock_writer = mocker.Mock()
    mocker.patch('csv.DictWriter', return_value=mock_writer)

    filtrar_labs_fga("pdf", "csv")
    
    assert mock_writer.writerows.called

def test_main_execucao(mocker):
    mocker.patch("os.path.exists", return_value=True)
    mock_filt = mocker.patch("scripts.extrair_labs_fga.filtrar_labs_fga")
    main()
    mock_filt.assert_called_once()

def test_main_falha_arquivo(mocker):
    mocker.patch("os.path.exists", return_value=False)
    with mocker.patch("builtins.print") as mock_print:
        main()
        mock_print.assert_called()