from scripts.extrair_labs_fga import extrair_palavra_chave, categorizar_lab

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