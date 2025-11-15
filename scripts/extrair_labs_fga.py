"""
Extrai e filtra informações de laboratórios da FGA a partir do PDF (parsing e heurísticas).
Gera CSV com laboratórios da FGA e remove duplicatas/ruído.
"""
import fitz  # PyMuPDF
import re
import csv
import os
import requests                     # Para fazer requisições HTTP (baixar HTML, baixar imagens)
from bs4 import BeautifulSoup       # Para "ler" e navegar pelo HTML das páginas web              # Para montar URLs completas (juntar URL base com caminhos relativos)
import urllib3                      # Usado internamente pelo requests, importamos para controlar avisos
from ddgs import DDGS               # Para fazer buscas na web usando o DuckDuckGo
from unidecode import unidecode     # Para remover acentos de textos (ex: "Robótica" -> "Robotica")
import time                         # Para adicionar pausas (sleep) no script
import random
from urllib.parse import urljoin, urlparse

# Desabilita avisos sobre certificados SSL inválidos (basicamente, quando certificados são inválidos e tem chance de ser scan)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Diretório onde este script (extrair_labs_fga.py) está localizado
SCRIPT_DIR = os.path.dirname(__file__)
# Caminho completo para a pasta onde as imagens dos laboratórios serão salvas
PASTA_IMAGENS_LABS = os.path.join(SCRIPT_DIR, "..", "data", "images", "labs")
# Este é o caminho que será salvo no CSV se a busca de imagem falhar.
# O caminho é relativo à pasta onde o CSV será salvo (data/Labs/)
CAMINHO_PLACEHOLDER = os.path.join("..", "data", "images", "placeholders", "default_lab.jpg")

# --- FUNÇÃO PARA EXTRAIR PALAVRA-CHAVE DO NOME ---

# Lista de palavras comuns (em minúsculo e sem acentos) que queremos ignorar
# ao determinar a palavra-chave principal de um laboratório.
STOP_WORDS = [
    'laboratorio', 'lab', 'de', 'e', 'da', 'do', 'dos', 'das', 'a', 'o',
    'em', 'para', 'com', 'sistemas', 'pesquisa', 'grupo', 'nucleo',
    'centro', 'automacao', 'aplicada', 'aplicados', 'estudos', 'avancados',
    'unb', 'fga'
    # Adicione mais palavras aqui se necessário
]

# --- DICIONÁRIO PARA CATEGORIZAÇÃO DE PLACEHOLDERS ---
CATEGORIAS_KEYWORDS = {
    # Categorias Principais (com 2 variações de placeholder cada)
    "software": [
        "software", "computacao", "computacional", "informática", "digital",
        "ia", "inteligencia artificial", "algoritmos", "dados", "bioinformatica"
    ],
    "eletronica": [
        "eletronica", "microeletronica", "hardware", "embarcados", "circuitos",
        "semicondutores", "telecomunicacoes"
    ],
    "mecanica_materiais": [ # Agrupa Automotiva, Aero, Energia, Materiais, Física
        "automotiva", "automotivo", "veicular", "aeroespacial", "aeronautica",
        "energia", "eletrica", "renovaveis", "potencia", "materiais", "nanotecnologia",
        "polimeros", "fisica", "mecanica", "controle", "robotica", "automacao" # Adicionei Robótica aqui também
    ],
    # A função categorizar_lab retornará "default" se nenhuma destas for encontrada
}

# --- FUNÇÃO PARA CATEGORIZAR LABORATÓRIO ---

def categorizar_lab(nome_do_lab):
    """
    Tenta classificar um laboratório em uma categoria pré-definida
    baseado em palavras-chave encontradas em seu nome.

    Usado para selecionar um placeholder mais relevante quando a busca
    de imagem real falha.

    Args:
        nome_do_lab (str): O nome completo do laboratório.

    Returns:
        str: O nome da categoria encontrada (ex: "software") ou "default".
    """
    try:
        nome_normalizado = unidecode(nome_do_lab.lower())

        # Itera sobre as categorias e suas palavras-chave definidas globalmente
        for categoria, keywords in CATEGORIAS_KEYWORDS.items():
            # any(...) retorna True se *qualquer* palavra-chave da lista for encontrada no nome
            if any(keyword in nome_normalizado for keyword in keywords):
                return categoria # Retorna o nome da categoria assim que encontrar a primeira correspondência

    except Exception as e:  # pylint: disable=broad-except
        print(f"    [Categorizar] Erro ao categorizar '{nome_do_lab}': {e}")
        # Em caso de erro, continua para retornar a categoria padrão

    # Se nenhum loop encontrou uma correspondência ou se houve erro
    return "default" # Retorna a categoria padrão

def extrair_palavra_chave(nome_do_lab):
    """
    Analisa um nome completo de laboratório e tenta extrair a palavra
    mais significativa (a "palavra-chave") para usar em buscas web.

    Processo:
    1. Normaliza o nome (minúsculas, sem acentos).
    2. Divide em palavras.
    3. Retorna a primeira palavra que não está na lista STOP_WORDS e é longa o suficiente.
    4. Se falhar, retorna a primeira palavra longa.
    5. Se falhar novamente, retorna uma chave genérica "pesquisa".

    Args:
        nome_do_lab (str): O nome completo do laboratório (ex: "Laboratório de Robótica").

    Returns:
        str: A palavra-chave extraída (ex: "robotica").
    """
    try:
        # 1. sem acento e minusculo
        nome_normalizado = unidecode(nome_do_lab.lower())

        # 2. Divide
        palavras = nome_normalizado.split()

        # 3. Filtra usando STOP_WORDS
        for palavra in palavras:
            # Verifica se não é stop word e tem um tamanho mínimo (evita 'ia', 'ti')
            if palavra not in STOP_WORDS and len(palavra) > 3:
                return palavra # Encontrou a palavra-chave principal

    except Exception as e:  # pylint: disable=broad-except
        # Em caso de erro inesperado durante o processamento do nome
        print(f"    [Palavra Chave] Erro ao extrair chave de '{nome_do_lab}': {e}")
        pass # Continua para retornar a chave genérica

    # 5. Plano C: Chave genérica (último recurso)
    print(f"    [Palavra Chave] Não foi possível extrair chave de '{nome_do_lab}'. Usando 'pesquisa'.")
    return "pesquisa"

# --- FUNÇÃO PARA BAIXAR IMAGEM DA WEB ---

def baixar_imagem(url_imagem, caminho_salvar):
    """
    Tenta baixar um arquivo de imagem a partir de uma URL e salvá-lo
    no caminho especificado.

    Args:
        url_imagem (str): A URL completa da imagem a ser baixada.
        caminho_salvar (str): O caminho completo no disco onde a imagem
                              deve ser salva (incluindo o nome do arquivo).

    Returns:
        bool: True se o download e salvamento foram bem-sucedidos, False caso contrário.
    """
    try:
        print(f"    [Download] Tentando baixar imagem de: {url_imagem}")
        # Headers para simular um navegador, importante para evitar bloqueios
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

        # Faz a requisição usando stream=True. Isso é crucial para arquivos
        # grandes (como imagens), pois baixa o conteúdo em "pedaços"
        # sem carregar tudo na memória de uma vez.
        response = requests.get(url_imagem, headers=headers, timeout=15, verify=False, stream=True)
        response.raise_for_status() # Verifica se a URL respondeu com sucesso (status 200 OK)

        # Verificação extra: Checa se o servidor está realmente enviando uma imagem
        content_type = response.headers.get('content-type')
        if not content_type or not content_type.startswith('image/'):
             print(f"    [Download] ⚠️ URL não retornou um tipo de conteúdo de imagem válido (recebido: {content_type}). Pulando download.")
             return False # Aborta se não for uma imagem

        # Garante que a pasta onde a imagem será salva exista.
        # os.path.dirname(caminho_salvar) pega o caminho da pasta (ex: data/images/labs/)
        # exist_ok=True evita erro se a pasta já existir.
        os.makedirs(os.path.dirname(caminho_salvar), exist_ok=True)

        # Abre o arquivo local no modo "escrita binária" ('wb')
        with open(caminho_salvar, 'wb') as f:
            # Itera sobre os "pedaços" (chunks) da resposta da imagem
            for chunk in response.iter_content(8192): # Lê em pedaços de 8KB
                if chunk: # Garante que o pedaço não está vazio
                    f.write(chunk) # Escreve o pedaço no arquivo local

        print(f"    [Download] ✅ Imagem salva com sucesso em: {caminho_salvar}")
        return True # Retorna True indicando sucesso

    # Tratamento de erros específicos para o download
    except requests.exceptions.Timeout:
        print(f"    [Download] ❌ Falha ao baixar {url_imagem}: A requisição demorou demais (Timeout).")
        return False
    except requests.exceptions.RequestException as e:
        # Captura outros erros de conexão, URL inválida, etc.
        print(f"    [Download] ❌ Falha ao baixar {url_imagem}: {e}")
        return False
    except Exception as e:  # pylint: disable=broad-except
        # Captura erros inesperados ao criar pasta, salvar arquivo, etc.
        print(f"    [Download] ❌ Erro inesperado durante o download/salvamento de {url_imagem}: {e}")
        return False

# --- FUNÇÃO PRINCIPAL: ENCONTRAR E BAIXAR IMAGEM PARA UM LAB ---

def encontrar_imagem_para_lab(nome_do_lab, pasta_base_imagem):
    """
    Orquestra o processo completo de encontrar uma imagem para um laboratório:
    1. Extrai a palavra-chave do nome.
    2. Busca na web pela homepage.
    3. Filtra os resultados para achar a URL mais relevante.
    4. Acessa a homepage e procura por uma imagem de destaque ("caça medalhas").
    5. Se encontrar a URL da imagem, chama a função para baixá-la.
    6. Retorna o caminho local da imagem baixada ou None se qualquer etapa falhar.

    Args:
        nome_do_lab (str): O nome completo do laboratório (vindo do PDF).
        pasta_base_imagem (str): O caminho da pasta onde as imagens baixadas
                                 devem ser salvas (ex: data/images/labs/).

    Returns:
        str or None: O caminho local completo para a imagem baixada
                     (ex: "data/images/labs/robotica.jpg") ou None se falhar.
    """

    URL_BLACKLIST = [
        "bing.com",
        "google.com",
        "escavador.com",
        "researchgate.net",
        "academia.edu",
        "github.com", 
        "linkedin.com",
        "facebook.com",
        "instagram.com",
        "twitter.com",
        "sigaa.unb.br" 
    ]

    IMAGE_FILENAME_BLACKLIST = [
        "logo-unb.png",
        "unbdpi-logo.png",
        "unbpi-logo.png",
        "logo_unb1.png",
        "pctec-unb_logo.png", 
        "repositoriocovid19_header.png", 
        "opine.png",
        "opine-sobre-o-portal.png", 
        "clipart/en.svg", 
        "antonio-150x150.jpg",     
        "cropped-face-12.png",     
        "foto_pessoal_moodles.png", 
        "googleusercontent.com/profile/picture", 
        "grade_curricular_atualizada.png", 
        "benvindo_rodrigues_pereira_junior.jpg",
    ]

    keyword = extrair_palavra_chave(nome_do_lab)

    query_de_busca = f'"{nome_do_lab}" OR site:unb.br "{keyword} FGA"'

    print(f"  [Busca Imagem] Buscando por: {query_de_busca} (chave: {keyword})")

    try:
        resultados_da_busca = []
        # Usa o gerenciador de contexto do DDGS para garantir fechamento
        with DDGS() as ddgs:
            # Faz a busca web, pedindo 5 resultados para o Brasil
            resultados_gen = ddgs.text(query_de_busca, region='br-pt', max_results=5)
            # Converte o gerador (promessa) em uma lista real, se houver resultados
            if resultados_gen:
                resultados_da_busca = list(resultados_gen)

        time.sleep(1.0) # Pausa de cortesia após a busca

        if not resultados_da_busca:
             print("    [Busca Imagem] ❌ Nenhum resultado encontrado na busca web.")
             return None # Se a busca falhar, não adianta continuar

        # --- FASE 2: FILTRO DE RELEVÂNCIA ---
        # --- FASE 2: FILTRO DE RELEVÂNCIA (V8 - Com Priorização e Blacklist) ---
        homepage_url = None
        print(f"    [Busca Imagem] Filtrando resultados por '{keyword}'...")

        url_prioritaria = None
        url_fallback = None
        url_ultimo_recurso = None

        for resultado in resultados_da_busca:
            url_original = resultado['href']
            url_lower = url_original.lower()
            titulo_lower_normalizado = unidecode(resultado['title'].lower())
            
            # 1. Verifica se a URL está na Blacklist
            if any(site_ruim in url_lower for site_ruim in URL_BLACKLIST):
                print(f"      [Filtro] Ignorando (Blacklist): {url_original}")
                continue # Pula este resultado, vai para o próximo

            # 2. Verifica se é um link de documento
            if any(ext in url_lower for ext in ['.pdf', '.doc', '.docx', '.odt']):
                print(f"      [Filtro] Ignorando (Documento): {url_original}")
                continue # Pula este resultado

            # 3. Salva o primeiro resultado válido (Plano C)
            if not url_ultimo_recurso:
                url_ultimo_recurso = url_original

            # 4. Verifica a relevância da palavra-chave
            keyword_no_titulo = keyword in titulo_lower_normalizado
            keyword_na_url = keyword in url_lower

            if keyword_no_titulo or keyword_na_url:
                # 5. PRIORIDADE MÁXIMA: É da UnB E tem a palavra-chave?
                if ".unb.br" in url_lower:
                    print(f"    [Busca Imagem] 🎯 Prioritário (UnB + Chave) encontrado: {url_original}")
                    url_prioritaria = url_original
                    break # Encontramos o melhor, para o loop
                
                # 6. Prioridade Média: Não é da UnB, mas tem a palavra-chave (Plano B)
                if not url_fallback:
                    print(f"    [Busca Imagem] ⚠️ Relevante (Externo + Chave) encontrado: {url_original}")
                    url_fallback = url_original

        # Decide qual URL usar, em ordem de prioridade
        if url_prioritaria:
            homepage_url = url_prioritaria   # 1º: UnB + Palavra-Chave
        elif url_fallback:
            homepage_url = url_fallback      # 2º: Externo + Palavra-Chave
        elif url_ultimo_recurso:
            homepage_url = url_ultimo_recurso # 3º: Primeiro link que não estava na blacklist
        else:
            print("    [Busca Imagem] ❌ Nenhum resultado web parece ser uma homepage válida (todos na blacklist?).")
            return None # Desiste

# --- FASE 3: CAÇA À IMAGEM (V11 - Priorização e Blacklist Aprimorada) ---
        print(f"    [Busca Imagem] Caçando imagem em: {homepage_url}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response_lab = requests.get(homepage_url, headers=headers, timeout=15, verify=False)
            response_lab.raise_for_status() 

            soup_lab = BeautifulSoup(response_lab.content, 'html.parser')
            url_imagem_encontrada = None 

            # --- Função helper V11 (agora interna da FASE 3) ---
            def is_url_valida(url_teste):
                if not url_teste:
                    return False
                url_lower = url_teste.lower()

                # 1. Rejeita 'data:' URIs (imagens embutidas que 'requests' não baixa)
                if url_lower.startswith('data:'):
                    print(f"      [Caça] ⚠️ Rejeitado (Data URI): {url_teste[:60]}...")
                    return False

                # 2. Rejeita se for SVG
                if url_lower.endswith('.svg'):
                    print(f"      [Caça] ⚠️ Rejeitado (SVG): {url_teste}")
                    return False

                # 3. Rejeita se estiver na blacklist de nomes de arquivo
                if any(nome_ruim in url_lower for nome_ruim in IMAGE_FILENAME_BLACKLIST):
                    print(f"      [Caça] ⚠️ Rejeitado (Blacklist Nome): {url_teste}")
                    return False

                return True
            # --- Fim da função helper ---

            # Alvo #1 (Ouro): Tag <meta property="og:image"> - SEMPRE A MAIOR PRIORIDADE
            meta_og_image = soup_lab.find('meta', property='og:image')
            if meta_og_image and meta_og_image.get('content'):
                url_teste = meta_og_image.get('content')
                if is_url_valida(url_teste):
                    url_imagem_encontrada = url_teste
                    print("      [Caça] 🥇 Ouro ('og:image')")

            # Alvo #2 (Verde): Primeira imagem GRANDE dentro do conteúdo principal (priorizar fotos de labs)
            # Busca agressiva por uma imagem que tenha pelo menos 200x200px
            if not url_imagem_encontrada:
                seletores_conteudo = ['main', 'article', 'div[class*="content"]', 'div[class*="post"]', 'body']
                for seletor in seletores_conteudo:
                    area_conteudo = soup_lab.select_one(seletor)
                    if area_conteudo:
                        for img_conteudo in area_conteudo.find_all('img'):
                            if img_conteudo and img_conteudo.get('src'):
                                url_teste = img_conteudo.get('src')
                                if is_url_valida(url_teste):
                                    # Tenta obter dimensões diretamente da tag, se existirem
                                    width_str = img_conteudo.get('width', '0').replace('px', '')
                                    height_str = img_conteudo.get('height', '0').replace('px', '')

                                    try:
                                        width = int(width_str)
                                        height = int(height_str)
                                        # MUDANÇA: Exige tamanho mínimo maior para conteúdo (200x200)
                                        if width >= 200 and height >= 200: 
                                            url_imagem_encontrada = url_teste
                                            print(f"      [Caça] 💚 Verde ('{seletor}' img >= 200px)")
                                            break 
                                    except ValueError:
                                        # Se width/height não são ints, pode ser que as dims não estejam na tag,
                                        # tentamos com o proximo loop
                                        pass
                            if url_imagem_encontrada: break 
                    if url_imagem_encontrada: break 

            # Alvo #3 (Prata): Imagem de Logo no Header (apenas se não achou og:image ou foto de conteúdo)
            # Este é mais um fallback para logos da homepage, não de labs específicos
            if not url_imagem_encontrada:
                seletores_logo = [
                    'img[id*="logo"]', 'img[class*="logo"]', 'img[src*="logo"]',
                    'img[id*="brand"]', 'img[class*="brand"]'
                ]
                for seletor in seletores_logo:
                    logo_img = soup_lab.select_one(seletor)
                    if logo_img and logo_img.get('src'):
                        url_teste = logo_img.get('src')

                        # NOVO: Extrai o domínio da homepage_url para verificação
                        domain_homepage = urlparse(homepage_url).netloc

                        if is_url_valida(url_teste):
                            # MUDANÇA V12: Se a URL da homepage NÃO FOR .unb.br E a imagem contiver "logo" no nome, REJEITAR.
                            # Isso evita pegar logos de outras universidades (ex: UFPE) como imagem para um lab da UnB.
                            if not domain_homepage.endswith('.unb.br') and "logo" in url_teste.lower():
                                print(f"      [Caça] ⚠️ Rejeitado (Logo Externo): {url_teste}")
                                continue # Pula esta imagem e tenta a próxima

                            width_str = logo_img.get('width', '0').replace('px', '')
                            height_str = logo_img.get('height', '0').replace('px', '')
                            try:
                                # Exige tamanho mínimo de 50px para logos
                                if int(width_str) > 50 or int(height_str) > 50: 
                                    url_imagem_encontrada = url_teste
                                    print(f"      [Caça] 🥈 Prata (Logo '{seletor}')")
                                    break
                            except ValueError: pass

            # Alvo #4 (Bronze): Primeira imagem maior que 100x100px dentro do <header> ou de um 'banner' (último recurso)
            if not url_imagem_encontrada:
                header = soup_lab.find('header')
                if header:
                    for img_header in header.find_all('img'): # Busca todas as imgs no header
                        if img_header and img_header.get('src'):
                            url_teste = img_header.get('src')
                            if is_url_valida(url_teste):
                                width_str = img_header.get('width', '0').replace('px', '')
                                height_str = img_header.get('height', '0').replace('px', '')
                                try:
                                    # MUDANÇA: Exige 100x100px para imgs no header/banner
                                    if int(width_str) > 100 and int(height_str) > 100: 
                                        url_imagem_encontrada = url_teste
                                        print("      [Caça] 🥉 Bronze (<header> img > 100px)")
                                        break
                                except ValueError: pass
                        if url_imagem_encontrada: break

                if not url_imagem_encontrada:
                    banner = soup_lab.find('div', class_=lambda x: x and 'banner' in x.lower())
                    if banner:
                        for img_banner in banner.find_all('img'): # Busca todas as imgs no banner
                            if img_banner and img_banner.get('src'):
                                url_teste = img_banner.get('src')
                                if is_url_valida(url_teste):
                                    width_str = img_banner.get('width', '0').replace('px', '')
                                    height_str = img_banner.get('height', '0').replace('px', '')
                                    try:
                                        if int(width_str) > 100 and int(height_str) > 100: 
                                            url_imagem_encontrada = url_teste
                                            print("      [Caça] 🥉 Bronze (banner div img > 100px)")
                                            break
                                    except ValueError: pass
                            if url_imagem_encontrada: break

            # --- FASE 4: DOWNLOAD E RETORNO DO RESULTADO ---
            if url_imagem_encontrada:
                url_imagem_completa = urljoin(homepage_url, url_imagem_encontrada)

                nome_base = "".join(c for c in keyword if c.isalnum() or c in ('_')).rstrip()
                nome_prefixo = "".join(c for c in nome_do_lab if c.isalnum())[:3].lower()
                nome_arquivo = f"{nome_prefixo}_{nome_base}.jpg" 

                caminho_local_salvar = os.path.join(pasta_base_imagem, nome_arquivo)

                # Chama a função de download
                if baixar_imagem(url_imagem_completa, caminho_local_salvar):
                    return caminho_local_salvar # SUCESSO!

            else:
                 print("      [Caça] ❌ Nenhuma imagem encontrada na página após todas as tentativas.")

        # Erros da "Caça" (Fase 3)
        except requests.exceptions.Timeout: # <--- NÍVEL 2 (ALINHADO COM O TRY INTERNO)
             print(f"    [Busca Imagem] ❌ Timeout ao acessar homepage {homepage_url}.")
        except requests.exceptions.RequestException as e: # <--- NÍVEL 2 (ALINHADO COM O TRY INTERNO)
            print(f"    [Busca Imagem] ❌ Erro de conexão/HTTP ao acessar homepage {homepage_url}: {e}")
        
        # --- LINHA DO ERRO ---
        # Esta linha deve estar no NÍVEL 1, (ALINHADA COM O TRY EXTERNO)
        print("    [Busca Imagem] ❌ Falha geral ao encontrar/baixar imagem para este laboratório.")
        return None 

    except Exception as e:  # pylint: disable=broad-except
        print(f"    [Busca Imagem] ❌ Erro inesperado durante o processo: {e}")
        return None

def limpar_texto(texto):
    """
    Remove caracteres especiais problemáticos do texto
    """
    if not texto:
        return texto
    # Remove espaços não-quebráveis e outros caracteres Unicode problemáticos
    texto = texto.replace('\u202f', ' ')  # Narrow no-break space
    texto = texto.replace('\xa0', ' ')    # Non-breaking space
    texto = texto.replace('\u2013', '-')  # En dash
    texto = texto.replace('\u2014', '-')  # Em dash
    texto = texto.replace('\u2019', "'")  # Right single quotation mark
    texto = texto.replace('\u201c', '"')  # Left double quotation mark
    texto = texto.replace('\u201d', '"')  # Right double quotation mark
    return texto

def juntar_palavras_hifenizadas(texto):
    """
    Remove hifenização de quebra de linha
    Exemplo: 'pesqui- sadores' -> 'pesquisadores'
    """
    if not texto:
        return texto
    # Padrão: letra + hífen + espaço(s) + letra minúscula
    # Isso indica quebra de palavra no final da linha
    texto = re.sub(r'(\w)-\s+(\w)', r'\1\2', texto)
    return texto

def extrair_laboratorios_fga_pdf(pdf_path, pagina_inicial=13):
    doc = fitz.open(pdf_path)
    idx_inicial = pagina_inicial - 1
    texto_completo = ""
    for num_pagina in range(idx_inicial, len(doc)):
        texto_pagina = doc[num_pagina].get_text()
        # Limpa caracteres especiais
        texto_completo += limpar_texto(texto_pagina)
    doc.close()
    # Lista para armazenar laboratórios
    laboratorios = []
    labs_fga = []
    # Divide o texto em linhas para análise
    linhas = texto_completo.split('\n')
    lab_atual = None
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        if not linha:
            i += 1
            continue
        
        # VERIFICA CABEÇALHOS DE SEÇÃO (antes de processar laboratórios)
        if (re.match(r'^\d+\.\d+(\.\d+)*\.', linha) or  # Numeração de seção (1.2.5.)
            re.match(r'^[_\-]{20,}$', linha)):  # Linha de separação longa
            # Salva o laboratório atual se existir
            if lab_atual:
                laboratorios.append(lab_atual)
                texto_completo_lab = f"{lab_atual['nome']} {lab_atual['coordenador']} {lab_atual['contato']} {lab_atual['descricao']}"
                if 'FGA' in texto_completo_lab.upper():
                    labs_fga.append(lab_atual)
                lab_atual = None
            i += 1
            continue
        
        # CASO ESPECIAL: Número sozinho em uma linha (labs 1-9)
        if re.match(r'^(\d+)\.$', linha):
            numero_lab = re.match(r'^(\d+)\.$', linha).group(1)
            if i + 1 < len(linhas):
                proxima_linha = linhas[i + 1].strip()
                if (proxima_linha and 
                    not proxima_linha.startswith('COORDENADOR:') and
                    not proxima_linha.startswith('COORDENADORES:') and
                    not proxima_linha.startswith('CONTATO:') and
                    not proxima_linha.startswith('DESCRIÇÃO:') and
                    not proxima_linha.startswith('DESCRICAO:')):
                    # Salva o laboratório anterior se existir
                    if lab_atual:
                        laboratorios.append(lab_atual)
                        # Verifica se é da FGA
                        texto_completo_lab = f"{lab_atual['nome']} {lab_atual['coordenador']} {lab_atual['contato']} {lab_atual['descricao']}"
                        if 'FGA' in texto_completo_lab.upper():
                            labs_fga.append(lab_atual)
                    # Cria novo laboratório
                    lab_atual = {
                        'nome': proxima_linha,
                        'coordenador': '',
                        'contato': '',
                        'descricao': ''
                    }
                    i += 2
                    continue
        
        # CASO NORMAL: Número e nome na mesma linha (labs 10+)
        padrao_numero_simples = re.match(r'^(\d+)\.\s+(.+)', linha)
        if padrao_numero_simples:
            numero_lab = padrao_numero_simples.group(1)
            nome_sem_numero = padrao_numero_simples.group(2).strip()
            # FILTRO 1: Rejeita sub-numeração
            if re.match(r'^\d+\.\d+', linha):
                i += 1
                continue

            # FILTRO 2: Rejeita cabeçalhos em MAIÚSCULAS
            palavras_significativas = [p for p in nome_sem_numero.split() 
                                       if len(p) > 2 and p.isalpha()]
            if palavras_significativas:
                maiusculas = sum(1 for p in palavras_significativas if p.isupper())
                if maiusculas / len(palavras_significativas) > 0.7:
                    i += 1
                    continue

            # Aceita se tiver pelo menos 10 caracteres e menos de 200
            if len(nome_sem_numero) > 10 and len(nome_sem_numero) < 200:
                # Se o nome termina com hífen, verifica se a sigla está na próxima linha
                if nome_sem_numero.endswith('-') and i + 1 < len(linhas):
                    proxima = linhas[i + 1].strip()
                    # Se a próxima linha é curta (provável sigla) e não é um campo, adiciona ao nome
                    if (proxima and len(proxima) < 30 and 
                        not proxima.startswith('COORDENADOR:') and
                        not proxima.startswith('COORDENADORES:') and
                        not proxima.startswith('CONTATO:') and
                        not proxima.startswith('DESCRIÇÃO:') and
                        not proxima.startswith('DESCRICAO:')):
                        nome_sem_numero += ' ' + proxima
                        i += 1  # Pula a próxima linha já que foi incorporada
                # Salva o laboratório anterior se existir
                if lab_atual:
                    laboratorios.append(lab_atual)
                    # Verifica se é da FGA
                    texto_completo_lab = f"{lab_atual['nome']} {lab_atual['coordenador']} {lab_atual['contato']} {lab_atual['descricao']}"
                    if 'FGA' in texto_completo_lab.upper():
                        labs_fga.append(lab_atual)
                # Cria novo laboratório
                lab_atual = {
                    'nome': nome_sem_numero,
                    'coordenador': '',
                    'contato': '',
                    'descricao': ''
                }
        # Se estamos rastreando um laboratório, tenta preencher informações
        elif lab_atual:
            # COORDENADOR ou COORDENADORES (singular e plural)
            if (linha.startswith('COORDENADOR:') or 
                linha.startswith('COORDENADORES:') or 
                linha.startswith('RESPONSÁVEL:') or
                linha.startswith('RESPONSÁVEIS:')):
                coordenador_texto = linha.split(':', 1)[1].strip() if ':' in linha else ''
                # Remove todos os IDs Lattes (pode haver múltiplos)
                coordenador_texto = re.sub(r'\s*\(ID Lattes:\s*\d+\)', '', coordenador_texto, flags=re.IGNORECASE)
                # Remove IDs Lattes incompletos (casos onde o parêntese fecha em outra linha)
                coordenador_texto = re.sub(r'\s*\(ID\s*$', '', coordenador_texto)
                coordenador_texto = re.sub(r'\s*\(ID Lattes:.*$', '', coordenador_texto)
                # Se já existe um coordenador, adiciona o novo separado por vírgula
                if lab_atual['coordenador']:
                    lab_atual['coordenador'] += ', ' + coordenador_texto.strip()
                else:
                    lab_atual['coordenador'] = coordenador_texto.strip()
            # CONTATO
            elif linha.startswith('CONTATO:'):
                lab_atual['contato'] = linha.split(':', 1)[1].strip() if ':' in linha else ''
            # DESCRIÇÃO
            elif linha.startswith('DESCRIÇÃO:') or linha.startswith('DESCRICAO:'):
                descricao = linha.split(':', 1)[1].strip() if ':' in linha else ''
                # Captura descrição em múltiplas linhas
                j = i + 1
                while j < len(linhas):
                    proxima_linha = linhas[j].strip()
                    # Verifica se encontrou cabeçalho de seção (termina processamento do lab atual)
                    if proxima_linha and re.match(r'^\d+\.\d+(\.\d+)*\.', proxima_linha):
                        break
                    
                    # Para se encontrar uma nova seção ou marcadores de fim
                    if proxima_linha and (':' in proxima_linha and 
                        any(proxima_linha.startswith(palavra) for palavra in 
                            ['GRUPOS', 'EQUIPAMENTOS', 'COORDENADOR', 'COORDENADORES', 
                             'CONTATO', 'LABORATÓRIO', 'NÚCLEO', 'CENTRO'])):
                        break

                    # Para se encontrar marcadores de rodapé ou nova seção
                    if proxima_linha:
                        # Detecta início de seção (letra + hífen + maiúsculas)
                        if re.match(r'^[IVX]+\s*-\s*[A-ZÀÁÂÃÉÊÍÓÔÕÚÇ\s]+$', proxima_linha):
                            break
                        # Detecta rodapé institucional
                        if any(palavra in proxima_linha.upper() for palavra in 
                               ['UNIVERSIDADE DE BRASÍLIA', 'PORTFÓLIO', 'INFRAESTRUTURA DE PESQUISA', 
                                'DPI CPAIP', 'CIÊNCIAS EXATAS E TECNOLÓGICAS', 'CIÊNCIAS EXATAS E DA TERRA']):
                            break

                        # Detecta linhas de separação (muitos underscores ou hífens)
                        if re.match(r'^[_\-]{10,}$', proxima_linha):
                            break

                        descricao += ' ' + proxima_linha
                    j += 1
                # Remove classificação
                descricao = re.sub(r'\s+CLASSIFICA[ÇC][ÃA]O:.*$', '', descricao, flags=re.IGNORECASE)
                descricao = re.sub(r'\s+Laborat[óo]rio de Pesquisa\s*$', '', descricao, flags=re.IGNORECASE)
                # Remove fragmentos de rodapé que podem ter sido capturados
                descricao = re.sub(r'\s+[IVX]+\s*-\s*CIÊNCIAS.*$', '', descricao, flags=re.IGNORECASE)
                descricao = re.sub(r'\s+UNIVERSIDADE DE BRASÍLIA.*$', '', descricao, flags=re.IGNORECASE)
                descricao = re.sub(r'\s+PORTFÓLIO.*$', '', descricao, flags=re.IGNORECASE)
                # Remove hifenização de quebra de linha
                descricao = juntar_palavras_hifenizadas(descricao)
                lab_atual['descricao'] = descricao.strip()
                i = j - 1
        i += 1
    # Adiciona o último laboratório
    if lab_atual:
        laboratorios.append(lab_atual)
        texto_completo_lab = f"{lab_atual['nome']} {lab_atual['coordenador']} {lab_atual['contato']} {lab_atual['descricao']}"
        if 'FGA' in texto_completo_lab.upper():
            labs_fga.append(lab_atual)
    return labs_fga

def filtrar_labs_fga(pdf_path, csv_saida):
    # Extrai laboratórios da FGA do PDF
    labs_fga = extrair_laboratorios_fga_pdf(pdf_path)
    # Detecta quando a descrição menciona um lab diferente do nome
    labs_fga_filtrados = []
    for lab in labs_fga:
        # Se a descrição menciona FGA, OK
        if 'FGA' in lab['descricao'].upper():
            # Verifica se a descrição fala de um lab diferente
            nome_curto = lab['nome'].split('-')[0].strip().split()[0:3]  # Primeiras palavras do nome
            primeira_frase_desc = lab['descricao'].split('.')[0] if lab['descricao'] else ""
            nome_keywords = [palavra.lower() for palavra in nome_curto if len(palavra) > 3]
            desc_lower = primeira_frase_desc.lower()
            # Verifica se pelo menos uma palavra do nome aparece na descrição
            tem_match = any(keyword in desc_lower for keyword in nome_keywords)
            sigla_match = re.match(r'^O\s+([A-Z]+),', primeira_frase_desc)
            if sigla_match:
                sigla_desc = sigla_match.group(1)
                if sigla_desc not in lab['nome']:
                    continue

            labs_fga_filtrados.append(lab)
    # Remove duplicatas baseando-se no nome do laboratório
    labs_unicos = {}
    for lab in labs_fga_filtrados:
        nome_normalizado = lab['nome'].strip().upper()
        if nome_normalizado not in labs_unicos:
            labs_unicos[nome_normalizado] = lab
    labs_fga_sem_id = list(labs_unicos.values())
    print()
    print(f"RESULTADO: {len(labs_fga_sem_id)} laboratorios da FGA ")
    print()

    # --- PASSO 1: ENRIQUECIMENTO COM IMAGENS (O SEU CÓDIGO) ---
    # (Usa 'labs_fga_sem_id' como entrada)
    print(f"\n--- Iniciando busca de imagens para os {len(labs_fga_sem_id)} laboratórios FGA encontrados ---")
    labs_enriquecidos = [] # Nova lista para guardar os labs com imagem

    for lab in labs_fga_sem_id: # <--- USA A VARIÁVEL DA 'main'
        print(f"\n---> Buscando imagem para: {lab['nome']}")
        caminho_imagem_local = encontrar_imagem_para_lab(lab['nome'], PASTA_IMAGENS_LABS)

        if caminho_imagem_local:
            lab['caminho_imagem'] = os.path.join("..", "images", "labs", os.path.basename(caminho_imagem_local))
            print(f"---> Imagem associada: {lab['caminho_imagem']}")
        else:
            categoria = categorizar_lab(lab['nome']) 
            if categoria in ["software", "eletronica", "mecanica_materiais", "default"]:
                numero_variacao = random.randint(1, 3)
                nome_placeholder = f"{categoria}_{numero_variacao}.jpg"
            else:
                numero_variacao = 1
                nome_placeholder = f"default_{numero_variacao}.jpg"
                categoria = "default"
            lab['caminho_imagem'] = os.path.join("..", "data", "images", "placeholders", nome_placeholder)
            print(f"---> Usando placeholder ({categoria} variação {numero_variacao}): {lab['caminho_imagem']}")

        labs_enriquecidos.append(lab) # Adiciona o lab (com imagem ou placeholder)
        time.sleep(1.5) 

    print("\n--- Busca de imagens concluída ---")

    # --- PASSO 2: GERAÇÃO DE IDS (O CÓDIGO DELES, DA MAIN) ---
    # (Usa 'labs_enriquecidos' como entrada)
    print("Gerando IDs únicos para os laboratórios...")
    labs_final_com_id = [] # Esta será a nova lista final com IDs

    for i, lab in enumerate(labs_enriquecidos): # <--- USA A LISTA ENRIQUECIDA
        contador = i + 1
        id_lab = f"2{contador:05d}" 

        # Cria um novo dicionário com o ID como primeiro campo
        lab_atualizado = {'id': id_lab, **lab}

        # Adiciona à nova lista final
        labs_final_com_id.append(lab_atualizado)

    print(f"✓ IDs gerados para {len(labs_final_com_id)} laboratórios.")

    # --- PASSO 3: SALVAR O CSV (A VERSÃO COMBINADA) ---
    if labs_final_com_id: # Verifica a lista final com IDs e Imagens
        # Salva no CSV de saída
        with open(csv_saida, 'w', newline='', encoding='utf-8') as f:
            # A lista de campos COMPLETA (a sua + a deles)
            campos = ['id', 'nome', 'coordenador', 'contato', 'descricao', 'caminho_imagem']
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            # Escreve a lista FINAL
            writer.writerows(labs_final_com_id)

def main():
    # Caminhos
    script_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(script_dir, "..", "data", "Labs", "Portfolio_Infraestrutura_UnB.pdf")
    csv_saida = os.path.join(script_dir, "..", "data", "Labs", "labs_fga.csv")
    # Verifica se o PDF existe
    if not os.path.exists(pdf_path):
        print(f"ERRO: PDF não encontrado em {pdf_path}")
        print("Baixe o PDF primeiro executando o script labs_pdf.py")
        return
    
    try:
        filtrar_labs_fga(pdf_path, csv_saida)
    except Exception as e:  # pylint: disable=broad-except
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
