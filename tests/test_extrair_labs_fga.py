from scripts.extrair_labs_fga import extrair_palavra_chave, categorizar_lab, limpar_texto, juntar_palavras_hifenizadas
import os
from scripts.extrair_labs_fga import (
    extrair_palavra_chave, categorizar_lab, limpar_texto, 
    juntar_palavras_hifenizadas, encontrar_imagem_para_lab
)
# --- Testes para a Função categorizar_lab ---

def test_categorizar_lab_software():
    """Testa se um lab de IA é categorizado como 'software'."""
    nome_lab = "Laboratório de Inteligência Artificial (AI Lab)"
    assert categorizar_lab(nome_lab) == "software"

def test_categorizar_lab_eletronica():
    """Testa se um lab de Microeletrônica é categorizado como 'eletronica'."""
    nome_lab = "Laboratório de Microeletrônica e Hardware"
    assert categorizar_lab(nome_lab) == "eletronica"

def test_categorizar_lab_mecanica_materiais():
    """Testa se um lab de Robótica é categorizado como 'mecanica_materiais'."""
    # (Baseado no dicionário que criamos, "robotica" está em "mecanica_materiais")
    nome_lab = "Núcleo de Robótica Aplicada"
    assert categorizar_lab(nome_lab) == "mecanica_materiais"

def test_categorizar_lab_fallback_default():
    """Testa se um nome não mapeado retorna 'default'."""
    nome_lab = "Laboratório de Coisas Químicas" # Não deve estar em nenhuma categoria
    assert categorizar_lab(nome_lab) == "default"


def test_limpar_texto_com_caracteres_especiais():
    """Testa a remoção de caracteres de espaço não-quebrável e outros."""
    texto_sujo = "Texto com espaço\xa0não-quebrável e traço\u2013estranho."
    texto_limpo = "Texto com espaço não-quebrável e traço-estranho."
    assert limpar_texto(texto_sujo) == texto_limpo

def test_limpar_texto_vazio_ou_nulo():
    """Testa se a função lida bem com entradas vazias ou nulas."""
    assert limpar_texto("") == ""
    assert limpar_texto(None) == None


def test_juntar_palavras_hifenizadas_sucesso():
    """Testa se a hifenização de quebra de linha é removida."""
    texto_hifenizado = "Esta é uma palavra que foi separa-\nda no final da linha."
    texto_correto = "Esta é uma palavra que foi separada no final da linha."
    assert juntar_palavras_hifenizadas(texto_hifenizado) == texto_correto

def test_juntar_palavras_hifenizadas_sem_hifen():
    """Testa se a função não altera texto normal."""
    texto_normal = "Este texto não tem hifenização."
    assert juntar_palavras_hifenizadas(texto_normal) == texto_normal


def test_encontrar_imagem_para_lab_fluxo_sucesso(mocker):
    """
    Testa o fluxo de sucesso completo da função 'encontrar_imagem_para_lab'.
    'mocker' é a ferramenta do pytest-mock que nos permite "fingir" (mockar)
    funções externas como chamadas de internet.
    """


    NOME_LAB_TESTE = "Laboratório de Robótica da FGA"
    PASTA_TESTE = "/tmp/fake-image-path" # Um caminho falso para o teste
    CAMINHO_FINAL_ESPERADO = os.path.join(PASTA_TESTE, "lab_robotica.jpg")

    mock_ddgs_instance = mocker.Mock()
    mock_ddgs_instance.text.return_value = [
        {'title': 'Laboratório de Robótica (LARA) UnB', 'href': 'http://lara.unb.br'}
    ]
    mocker.patch('scripts.extrair_labs_fga.DDGS', return_value=mock_ddgs_instance)

    mock_response_html = mocker.Mock()
    mock_response_html.content = '<html><body><img src="/logo-do-lab.png"></body></html>'
    mock_response_html.raise_for_status = mocker.Mock() # Finge que o site retornou 200 OK
    mocker.patch('scripts.extrair_labs_fga.requests.get', return_value=mock_response_html)

    mocker.patch('scripts.extrair_labs_fga.baixar_imagem', return_value=True)

    mocker.patch('scripts.extrair_labs_fga.urljoin', return_value="http://lara.unb.br/logo-do-lab.png")

    caminho_retornado = encontrar_imagem_para_lab(NOME_LAB_TESTE, PASTA_TESTE)

    scripts.extrair_labs_fga.baixar_imagem.assert_called_once_with(
        "http://lara.unb.br/logo-do-lab.png", 
        CAMINHO_FINAL_ESPERADO
    )

    assert caminho_retornado == CAMINHO_FINAL_ESPERADO
