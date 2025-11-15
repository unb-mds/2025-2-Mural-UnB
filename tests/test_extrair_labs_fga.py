from scripts.extrair_labs_fga import extrair_palavra_chave, categorizar_lab, limpar_texto, juntar_palavras_hifenizadas

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

# --- Testes para a Função limpar_texto ---

def test_limpar_texto_com_caracteres_especiais():
    """Testa a remoção de caracteres de espaço não-quebrável e outros."""
    texto_sujo = "Texto com espaço\xa0não-quebrável e traço\u2013estranho."
    texto_limpo = "Texto com espaço não-quebrável e traço-estranho."
    assert limpar_texto(texto_sujo) == texto_limpo

def test_limpar_texto_vazio_ou_nulo():
    """Testa se a função lida bem com entradas vazias ou nulas."""
    assert limpar_texto("") == ""
    assert limpar_texto(None) == None

# --- Testes para a Função juntar_palavras_hifenizadas ---

def test_juntar_palavras_hifenizadas_sucesso():
    """Testa se a hifenização de quebra de linha é removida."""
    texto_hifenizado = "Esta é uma palavra que foi separa-\nda no final da linha."
    texto_correto = "Esta é uma palavra que foi separada no final da linha."
    assert juntar_palavras_hifenizadas(texto_hifenizado) == texto_correto

def test_juntar_palavras_hifenizadas_sem_hifen():
    """Testa se a função não altera texto normal."""
    texto_normal = "Este texto não tem hifenização."
    assert juntar_palavras_hifenizadas(texto_normal) == texto_normal