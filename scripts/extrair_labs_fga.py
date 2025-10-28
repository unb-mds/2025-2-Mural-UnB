import fitz  # PyMuPDF
import re
import csv
import os
import requests                     # Para fazer requisições HTTP (baixar HTML, baixar imagens)
from bs4 import BeautifulSoup       # Para "ler" e navegar pelo HTML das páginas web
import urllib.parse                 # Para montar URLs completas (juntar URL base com caminhos relativos)
import urllib3                      # Usado internamente pelo requests, importamos para controlar avisos
from ddgs import DDGS               # Para fazer buscas na web usando o DuckDuckGo
from unidecode import unidecode     # Para remover acentos de textos (ex: "Robótica" -> "Robotica")
import time                         # Para adicionar pausas (sleep) no script

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
    "software": [
        "software", "computacao", "computacional", "informática", "digital",
        "ia", "inteligencia artificial", "algoritmos", "dados", "bioinformatica"
    ],
    "eletronica": [
        "eletronica", "microeletronica", "hardware", "embarcados", "circuitos",
        "semicondutores", "telecomunicacoes"
    ],
    "automotiva": [
        "automotiva", "automotivo", "veicular", "veiculo", "motor", "combustao",
        "transporte"
    ],
    "aeroespacial": [
        "aeroespacial", "aeronautica", "espacial", "satelite", "foguete",
        "aerodinamica", "propulsao"
    ],
    "energia": [
        "energia", "eletrica", "renovaveis", "potencia", "fotovoltaica",
        "solar", "redes", "eficiencia energetica"
    ],
    "robotica": [
        "robotica", "automacao", "mecatronica", "controle", "robo", "drone",
        "manipuladores"
    ],
    "fisica": [
        "fisica", "astrofisica", "cosmologia", "optica", "plasma",
        "espectroscopia", "acustica", "biofisica"
    ],
    "materiais": [
        "materiais", "nanotecnologia", "polimeros", "ceramica", "compósitos",
        "metalurgia"
    ],
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

    except Exception as e:
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

        # 4. Plano B: Primeira palavra longa (se o filtro não achar nada útil)
        for palavra in palavras:
             if len(palavra) > 4:
                return palavra # Retorna a primeira palavra com mais de 4 letras

    except Exception as e:
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
    except Exception as e:
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

    # --- FASE 1: PREPARAÇÃO E BUSCA WEB ---
    # Usa a função extrair_palavra_chave para obter a palavra-chave
    keyword = extrair_palavra_chave(nome_do_lab)
    # Monta uma query de busca: tenta o nome exato OU busca no site da unb pela chave + FGA
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
        homepage_url = None # Onde guardaremos a URL vencedora
        print(f"    [Busca Imagem] Filtrando resultados por '{keyword}'...")

        for resultado in resultados_da_busca:
            # Normaliza (minúsculo, sem acentos) para comparação robusta
            titulo_normalizado = unidecode(resultado['title'].lower())
            url_normalizada = unidecode(resultado['href'].lower())

            # Condição do filtro: Palavra-chave no título OU na URL E NÃO é link de documento
            if (keyword in titulo_normalizado or keyword in url_normalizada) and \
               not any(ext in url_normalizada for ext in ['.pdf', '.doc', '.docx', '.odt']):
                homepage_url = resultado['href'] # Guarda a URL original
                print(f"    [Busca Imagem] 🎯 Relevante encontrado: {homepage_url}")
                break # Para no primeiro resultado relevante

        # Plano B: Se o filtro não achou nada com a palavra-chave
        if not homepage_url:
            for resultado in resultados_da_busca:
                 url_normalizada = unidecode(resultado['href'].lower())
                 # Pega o primeiro resultado que não seja link de documento
                 if not any(ext in url_normalizada for ext in ['.pdf', '.doc', '.docx', '.odt']):
                      homepage_url = resultado['href']
                      print(f"    [Busca Imagem] ⚠️ Filtro falhou. Usando primeiro resultado válido: {homepage_url}")
                      break

        # Plano C: Se nem o plano B funcionou (só achou links de documentos?)
        if not homepage_url:
             print("    [Busca Imagem] ❌ Nenhum resultado web parece ser uma homepage válida.")
             return None 

        # --- FASE 3: CAÇA À IMAGEM NA HOMEPAGE SELECIONADA ---
        print(f"    [Busca Imagem] Caçando imagem em: {homepage_url}")
        try:
            # Prepara headers e faz a requisição para a homepage
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response_lab = requests.get(homepage_url, headers=headers, timeout=15, verify=False)
            response_lab.raise_for_status() # Verifica se a página respondeu OK

            # Prepara o BeautifulSoup para ler o HTML da página
            soup_lab = BeautifulSoup(response_lab.content, 'html.parser')
            url_imagem_encontrada = None # Onde guardaremos a URL da imagem achada

            # Alvo #1 (Ouro): Tag <meta property="og:image"> (padrão para compartilhamento)
            meta_og_image = soup_lab.find('meta', property='og:image')
            if meta_og_image and meta_og_image.get('content'):
                url_imagem_encontrada = meta_og_image.get('content')
                print("      [Caça] 🥇 Ouro ('og:image')")

            # Alvo #2 (Prata): Imagem de Logo (busca por 'logo' ou 'brand')
            if not url_imagem_encontrada:
                seletores_logo = [
                    'img[id*="logo"]', 'img[class*="logo"]', 'img[src*="logo"]',
                    'img[id*="brand"]', 'img[class*="brand"]'
                ]
                for seletor in seletores_logo:
                    logo_img = soup_lab.select_one(seletor)
                    if logo_img and logo_img.get('src'):
                        # Verifica se a imagem não é muito pequena (evita ícones)
                        width = logo_img.get('width', '0').replace('px', '')
                        height = logo_img.get('height', '0').replace('px', '')
                        try:
                           if int(width) > 30 or int(height) > 30: # Ajuste o tamanho mínimo se necessário
                                url_imagem_encontrada = logo_img.get('src')
                                print(f"      [Caça] 🥈 Prata (seletor: '{seletor}')")
                                break
                        except ValueError: pass # Ignora width/height não numéricos

            # Alvo #3 (Bronze): Imagem dentro do <header> ou de um 'banner'
            if not url_imagem_encontrada:
                header = soup_lab.find('header')
                if header:
                    img_header = header.find('img')
                    if img_header and img_header.get('src'):
                        url_imagem_encontrada = img_header.get('src')
                        print("      [Caça] 🥉 Bronze (<header> img)")
                if not url_imagem_encontrada: # Só procura banner se não achar no header
                    banner = soup_lab.find('div', class_=lambda x: x and 'banner' in x.lower())
                    if banner:
                        img_banner = banner.find('img')
                        if img_banner and img_banner.get('src'):
                            url_imagem_encontrada = img_banner.get('src')
                            print("      [Caça] 🥉 Bronze (banner div img)")

            # Alvo #4 (Cobre): Primeira imagem grande dentro do conteúdo principal
            if not url_imagem_encontrada:
                seletores_conteudo = ['main', 'article', 'div[class*="content"]', 'div[class*="post"]', 'body'] # Adicionado 'body' como último recurso
                for seletor in seletores_conteudo:
                    area_conteudo = soup_lab.select_one(seletor)
                    if area_conteudo:
                        img_conteudo = area_conteudo.find('img')
                        if img_conteudo and img_conteudo.get('src'):
                            # Verifica se a imagem é razoavelmente grande
                            width = img_conteudo.get('width', '0').replace('px', '')
                            height = img_conteudo.get('height', '0').replace('px', '')
                            try:
                               if int(width) > 50 or int(height) > 50: # Ajuste o tamanho mínimo
                                    url_imagem_encontrada = img_conteudo.get('src')
                                    print(f"      [Caça] 🥉 Cobre ('{seletor}' img)")
                                    break
                            except ValueError: pass

            # --- FASE 4: DOWNLOAD E RETORNO DO RESULTADO ---
            if url_imagem_encontrada:
                # Garante que a URL da imagem seja absoluta
                url_imagem_completa = urllib.parse.urljoin(homepage_url, url_imagem_encontrada)

                # Cria um nome de arquivo "seguro" e mais descritivo
                # Remove caracteres inválidos da palavra-chave
                nome_base = "".join(c for c in keyword if c.isalnum() or c in ('_')).rstrip()
                # Pega as 3 primeiras letras do nome do lab (seguro para nomes de arquivo)
                nome_prefixo = "".join(c for c in nome_do_lab if c.isalnum())[:3].lower()
                # Combina: ex -> "lab_robotica.jpg"
                nome_arquivo = f"{nome_prefixo}_{nome_base}.jpg" # Assume JPG, pode melhorar depois

                # Monta o caminho completo onde a imagem será salva
                caminho_local_salvar = os.path.join(pasta_base_imagem, nome_arquivo)

                # Chama a função de download (do Commit 3)
                if baixar_imagem(url_imagem_completa, caminho_local_salvar):
                    # Se o download deu certo, retorna o caminho local
                    return caminho_local_salvar

            else:
                 print("      [Caça] ❌ Nenhuma imagem encontrada na página após todas as tentativas.")


        except requests.exceptions.Timeout:
             print(f"    [Busca Imagem] ❌ Timeout ao acessar homepage {homepage_url}.")
        except requests.exceptions.RequestException as e:
            print(f"    [Busca Imagem] ❌ Erro de conexão/HTTP ao acessar homepage {homepage_url}: {e}")

        # Se chegou aqui, alguma etapa falhou (busca, filtro, caça ou download)
        print("    [Busca Imagem] ❌ Falha geral ao encontrar/baixar imagem para este laboratório.")
        return None # Retorna None para indicar falha

    except Exception as e:
        # Captura erros inesperados na busca DDGS ou na lógica de filtro
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
    labs_fga_final = list(labs_unicos.values())
    print()
    print(f"RESULTADO: {len(labs_fga_final)} laboratorios da FGA ")
    print()
# --- ENRIQUECIMENTO COM IMAGENS (NOVO LOCAL) ---
    print(f"\n--- Iniciando busca de imagens para os {len(labs_fga_final)} laboratórios FGA encontrados ---")
    labs_enriquecidos = [] # Nova lista para guardar os labs com imagem

    for lab in labs_fga_final:
        print(f"\n---> Buscando imagem para: {lab['nome']}")
        # Chama a função principal para encontrar/baixar a imagem
        caminho_imagem_local = encontrar_imagem_para_lab(lab['nome'], PASTA_IMAGENS_LABS)

        if caminho_imagem_local:
            # SUCESSO! Monta o caminho relativo para o CSV
            lab['caminho_imagem'] = os.path.join("..", "images", "labs", os.path.basename(caminho_imagem_local))
            print(f"---> Imagem associada: {lab['caminho_imagem']}")
        else:
            # FALHA! Usa o placeholder
            lab['caminho_imagem'] = CAMINHO_PLACEHOLDER
            print(f"---> Usando placeholder: {lab['caminho_imagem']}")

        # Adiciona o laboratório (agora com a chave 'caminho_imagem') à nova lista
        labs_enriquecidos.append(lab)

        time.sleep(1.5) # Pausa educada entre as buscas

    print("\n--- Busca de imagens concluída ---")
    # --- FIM DO ENRIQUECIMENTO ---

    # Agora, a escrita do CSV usa a lista 'labs_enriquecidos'
    if labs_enriquecidos: # Verifica a nova lista
        # Salva no CSV de saída
        with open(csv_saida, 'w', newline='', encoding='utf-8') as f:
            # A lista de campos já está correta (inclui 'caminho_imagem')
            campos = ['nome', 'coordenador', 'contato', 'descricao', 'caminho_imagem']
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            # USA A NOVA LISTA AQUI!
            writer.writerows(labs_enriquecidos)

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
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
