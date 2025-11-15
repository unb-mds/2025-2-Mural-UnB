import pytest
import os
import random
import csv

import scripts.extrair_labs_fga

from scripts.extrair_labs_fga import (
    extrair_palavra_chave,
    categorizar_lab,
    limpar_texto,
    juntar_palavras_hifenizadas,
    encontrar_imagem_para_lab,
    filtrar_labs_fga
)


def test_extrair_palavra_chave_sucesso():
    nome_lab = "Laboratório de Robótica e Sistemas Embarcados"
    assert extrair_palavra_chave(nome_lab) == "robotica"

def test_extrair_palavra_chave_sem_chave():
    nome_lab = "Laboratório de Pesquisa da UnB" # Todas são stop words
    assert extrair_palavra_chave(nome_lab) == "pesquisa"



def test_categorizar_lab_software():
    nome_lab = "Laboratório de Inteligência Artificial (AI Lab)"
    assert categorizar_lab(nome_lab) == "software"

def test_categorizar_lab_eletronica():
    nome_lab = "Laboratório de Microeletrônica e Hardware"
    assert categorizar_lab(nome_lab) == "eletronica"

def test_categorizar_lab_mecanica_materiais():
    nome_lab = "Núcleo de Robótica Aplicada"
    assert categorizar_lab(nome_lab) == "mecanica_materiais"

def test_categorizar_lab_fallback_default():
    nome_lab = "Laboratório de Coisas Químicas"
    assert categorizar_lab(nome_lab) == "default"


def test_limpar_texto_com_caracteres_especiais():
    texto_sujo = "Texto com espaço\xa0não-quebrável e traço\u2013estranho."
    texto_limpo = "Texto com espaço não-quebrável e traço-estranho."
    assert limpar_texto(texto_sujo) == texto_limpo

def test_limpar_texto_vazio_ou_nulo():
    assert limpar_texto("") == ""
    assert limpar_texto(None) == None

def test_juntar_palavras_hifenizadas_sucesso():
    texto_hifenizado = "Esta é uma palavra que foi separa-\nda no final da linha."
    texto_correto = "Esta é uma palavra que foi separada no final da linha."
    assert juntar_palavras_hifenizadas(texto_hifenizado) == texto_correto

def test_juntar_palavras_hifenizadas_sem_hifen():
    texto_normal = "Este texto não tem hifenização."
    assert juntar_palavras_hifenizadas(texto_normal) == texto_normal



def test_encontrar_imagem_para_lab_fluxo_sucesso(mocker):
    NOME_LAB_TESTE = "Laboratório de Robótica da FGA"
    PASTA_TESTE = "/tmp/fake-image-path"
    CAMINHO_FINAL_ESPERADO = os.path.join(PASTA_TESTE, "lab_robotica.jpg")

    mock_ddgs_class = mocker.patch('scripts.extrair_labs_fga.DDGS')
    mock_ddgs_instance = mocker.Mock()
    mock_ddgs_instance.text.return_value = [{'title': 'Laboratório de Robótica (LARA) UnB', 'href': 'http://lara.unb.br'}]
    mock_ddgs_class.return_value.__enter__.return_value = mock_ddgs_instance
    mock_ddgs_class.return_value.__exit__ = mocker.Mock()

    
    mock_response_html = mocker.Mock()
    mock_response_html.content = '<html><body><main><img src="/foto-real.jpg" width="250" height="250"></main></body></html>'
    mock_response_html.raise_for_status = mocker.Mock()
    mocker.patch('scripts.extrair_labs_fga.requests.get', return_value=mock_response_html)

    mock_baixar = mocker.patch('scripts.extrair_labs_fga.baixar_imagem', return_value=True)
    mocker.patch('scripts.extrair_labs_fga.urljoin', return_value="http://lara.unb.br/foto-real.jpg")    

    caminho_retornado = encontrar_imagem_para_lab(NOME_LAB_TESTE, PASTA_TESTE)
    
    # Verifica
    mock_baixar.assert_called_once_with(
    "http://lara.unb.br/foto-real.jpg", # <-- URL Atualizada
    CAMINHO_FINAL_ESPERADO
    )
    assert caminho_retornado == CAMINHO_FINAL_ESPERADO


def test_encontrar_imagem_para_lab_falha_na_busca_web(mocker):
    mock_ddgs_instance = mocker.Mock()
    mock_ddgs_instance.text.return_value = [] # Lista vazia
    mocker.patch('scripts.extrair_labs_fga.DDGS', return_value=mock_ddgs_instance)
    
    mock_requests_get = mocker.patch('scripts.extrair_labs_fga.requests.get')
    mock_baixar_imagem = mocker.patch('scripts.extrair_labs_fga.baixar_imagem')

    caminho_retornado = encontrar_imagem_para_lab("Nome de Lab Falso", "/caminho/falso")

    assert caminho_retornado is None
    mock_requests_get.assert_not_called()
    mock_baixar_imagem.assert_not_called()


def test_filtrar_labs_fga_usa_placeholder_corretamente(mocker):
    mock_lab_do_pdf = {
        'nome': 'Laboratório de Inteligência Artificial',
        'coordenador': 'Prof. Teste',
        'contato': 'teste@unb.br',
        'descricao': 'Um lab de software da FGA.'
    }
    mocker.patch('scripts.extrair_labs_fga.extrair_laboratorios_fga_pdf', return_value=[mock_lab_do_pdf])
    mocker.patch('scripts.extrair_labs_fga.encontrar_imagem_para_lab', return_value=None)
    mocker.patch('scripts.extrair_labs_fga.random.randint', return_value=3)
    
    mock_writer = mocker.Mock()
    mocker.patch('csv.DictWriter', return_value=mock_writer)
    mocker.patch('builtins.open', mocker.mock_open())

    filtrar_labs_fga("caminho/falso.pdf", "caminho/falso.csv")

    caminho_placeholder_esperado = os.path.join("..", "data", "images", "placeholders", "software_3.jpg")
    lab_final_esperado = {
        'id': '200001', 
        'nome': 'Laboratório de Inteligência Artificial',
        'coordenador': 'Prof. Teste',
        'contato': 'teste@unb.br',
        'descricao': 'Um lab de software da FGA.',
        'caminho_imagem': caminho_placeholder_esperado
    }
    
    mock_writer.writerows.assert_called_once_with([lab_final_esperado])