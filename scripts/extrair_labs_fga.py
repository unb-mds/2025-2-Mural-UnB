import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib3
from ddgs import DDGS
from unidecode import unidecode
import time
import fitz  # PyMuPDF
import re
import csv
import os

    # Desabilita os avisos de segurança sobre certificados SSL inválidos
    # (Seu script vai acessar muitos sites, é bom ter isso)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # --- MÓDULO DE BUSCA DE IMAGEM ---

    # Lista de palavras comuns que queremos ignorar ao buscar
    # Sinta-se à vontade para adicionar mais palavras aqui se notar "ruído"
STOP_WORDS = [
    'laboratorio', 'lab', 'de', 'e', 'da', 'do', 'dos', 'das', 'a', 'o',
    'em', 'para', 'com', 'sistemas', 'pesquisa', 'grupo', 'nucleo', 
    'centro', 'automacao', 'aplicada', 'aplicados', 'estudos', 'avancados',
    'unb', 'fga'
]

SCRIPT_DIR = os.path.dirname(__file__)
PASTA_IMAGENS_LABS = os.path.join(SCRIPT_DIR, "..", "data", "images", "labs")
CAMINHO_PLACEHOLDER = os.path.join("..", "data", "images", "placeholders", "default_lab.jpg") # fazer o caminho das imagens placeholder

def extrair_palavra_chave(nome_do_lab):
    """
    Pega um nome de laboratório completo e extrai a palavra-chave mais importante.
    Ex: "Laboratório de Robótica e Sistemas Embarcados" -> "robotica"
    Ex: "Laboratório de Microeletrônica" -> "microeletronica"
    """
    try:
        # 1. Normaliza: Converte para minúsculo e remove acentos
        # Ex: "Laboratório de Robótica" -> "laboratorio de robotica"
        nome_normalizado = unidecode(nome_do_lab.lower())
        
        # 2. Divide o nome em palavras individuais
        # Ex: ["laboratorio", "de", "robotica"]
        palavras = nome_normalizado.split()
        
        # 3. Filtra as palavras
        for palavra in palavras:
            # Se a palavra NÃO ESTÁ na lista de stop words E tem mais de 3 letras...
            if palavra not in STOP_WORDS and len(palavra) > 3:
                # ...nós a encontramos!
                return palavra # Ex: "robotica"
                
        # 4. Plano B (Se o filtro falhar)
        # Se não encontrar, apenas retorna a primeira palavra "longa"
        for palavra in palavras:
            if len(palavra) > 4:
                return palavra # Ex: "microeletronica" (se 'microeletronica' não estivesse nas stop words)

    except Exception:
        # Se tudo der errado, retorna uma chave genérica
        pass

    # 5. Plano C (Último recurso)
    # Retorna uma palavra-chave genérica que sempre dará algum resultado
    return "pesquisa"

def baixar_imagem(url_imagem, caminho_salvar):
    """
    Tenta baixar uma imagem de uma URL e salvá-la localmente.
    Retorna True se for bem-sucedido, False se falhar.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        # Usamos stream=True para baixar a imagem "em pedaços"
        response = requests.get(url_imagem, headers=headers, timeout=10, verify=False, stream=True)
        response.raise_for_status()

        # Cria a pasta de destino se ela não existir
        os.makedirs(os.path.dirname(caminho_salvar), exist_ok=True)
        
        # Salva a imagem no arquivo
        with open(caminho_salvar, 'wb') as f:
            for chunk in response.iter_content(8192): # Salva em pedaços de 8KB
                f.write(chunk)
        
        print(f"    [Download] ✅ Imagem salva em: {caminho_salvar}")
        return True # Sucesso!
        
    except Exception as e:
        print(f"    [Download] ❌ Falha ao baixar {url_imagem}: {e}")
        return False # Falha


def encontrar_imagem_para_lab(nome_do_lab, pasta_base_imagem):
    """
    Recebe um nome de laboratório, busca na web, filtra,
    ENCONTRA a URL, BAIXA a imagem e RETORNA o caminho local.
    """
    
    # 1. Gera a palavra-chave dinamicamente
    keyword = extrair_palavra_chave(nome_do_lab)
    query_de_busca = f'"{nome_do_lab}" OR "{keyword} FGA UnB"'
    
    print(f"  [Busca Imagem] Buscando por: {query_de_busca} (chave: {keyword})")
    
    try:
        resultados_da_busca = []
        with DDGS() as ddgs:
            resultados_gen = ddgs.text(query_de_busca, region='br-pt', max_results=5)
            if resultados_gen:
                resultados_da_busca = list(resultados_gen)
        
        time.sleep(1.0) # Pausa de cortesia

        if resultados_da_busca:
            homepage_url = None
            
            for resultado in resultados_da_busca:
                titulo_normalizado = unidecode(resultado['title'].lower())
                url_normalizada = unidecode(resultado['href'].lower())
                
                if keyword in titulo_normalizado or keyword in url_normalizada:
                    homepage_url = resultado['href']
                    break 
            
            if not homepage_url:
                homepage_url = resultados_da_busca[0]['href']
            
            # --- Início da Caça à Imagem ---
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
                response_lab = requests.get(homepage_url, headers=headers, timeout=10, verify=False)
                response_lab.raise_for_status() 

                soup_lab = BeautifulSoup(response_lab.content, 'html.parser')
                url_imagem_encontrada = None

                # Alvo #1: 'og:image'
                meta_og_image = soup_lab.find('meta', property='og:image')
                if meta_og_image and meta_og_image.get('content'):
                    url_imagem_encontrada = meta_og_image.get('content')

                # Alvo #2: Logo
                if not url_imagem_encontrada:
                    seletores_logo = [
                        'img[id*="logo"]', 'img[class*="logo"]', 'img[src*="logo"]',
                        'img[id*="brand"]', 'img[class*="brand"]'
                    ]
                    for seletor in seletores_logo:
                        logo_img = soup_lab.select_one(seletor)
                        if logo_img and logo_img.get('src'):
                            url_imagem_encontrada = logo_img.get('src')
                            break

                # Alvo #3: Header/Banner
                if not url_imagem_encontrada:
                    header = soup_lab.find('header')
                    if header:
                        img_header = header.find('img')
                        if img_header and img_header.get('src'):
                            url_imagem_encontrada = img_header.get('src')
                    if not url_imagem_encontrada:
                        banner = soup_lab.find('div', class_=lambda x: x and 'banner' in x.lower())
                        if banner:
                            img_banner = banner.find('img')
                            if img_banner and img_banner.get('src'):
                                url_imagem_encontrada = img_banner.get('src')

                # Alvo #4: Conteúdo
                if not url_imagem_encontrada:
                    seletores_conteudo = ['main', 'article', 'div[class*="content"]', 'div[class*="post"]']
                    for seletor in seletores_conteudo:
                        area_conteudo = soup_lab.select_one(seletor)
                        if area_conteudo:
                            img_conteudo = area_conteudo.find('img')
                            if img_conteudo and img_conteudo.get('src'):
                                url_imagem_encontrada = img_conteudo.get('src')
                                break
                
                # --- Resultado da Caça ---
                if url_imagem_encontrada:
                    url_imagem_completa = urllib.parse.urljoin(homepage_url, url_imagem_encontrada)
                    
                    # --- NOVO BLOCO DE DOWNLOAD ---
                    # 1. Cria um nome de arquivo "seguro" a partir da palavra-chave
                    nome_arquivo = f"{keyword}.jpg" # Ex: "robotica.jpg"
                    
                    # 2. Define o caminho completo para salvar
                    caminho_local_salvar = os.path.join(pasta_base_imagem, nome_arquivo)
                    
                    # 3. Tenta baixar
                    if baixar_imagem(url_imagem_completa, caminho_local_salvar):
                        return caminho_local_salvar # Retorna o CAMINHO LOCAL
                    # Se o download falhar, ele continua e retorna None
                    
            except requests.exceptions.RequestException as e:
                print(f"    [Busca Imagem] ❌ Erro ao acessar homepage {homepage_url}: {e}")

    except Exception as e:
        print(f"    [Busca Imagem] ❌ Erro geral na busca: {e}")
    
    # Se qualquer coisa falhar, retorna None
    print("    [Busca Imagem] ❌ Nenhuma imagem encontrada.")
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
                        # a integração da imagem
                    print(f"\nIniciando busca de imagem para: {lab_atual['nome']}")
                    caminho_imagem_local = encontrar_imagem_para_lab(lab_atual['nome'], PASTA_IMAGENS_LABS)
                    
                    if caminho_imagem_local:
                        # Solução 2: Imagem baixada!
                        # Precisamos salvar o caminho relativo ao CSV (que está em ../Labs)
                        lab_atual['caminho_imagem'] = os.path.join("..", "images", "labs", os.path.basename(caminho_imagem_local))
                    else:
                        # Solução 1: Placeholder
                        lab_atual['caminho_imagem'] = CAMINHO_PLACEHOLDER
                    
                    time.sleep(1.5) # Para não sobrecarregar
                    # --- FIM DA INTEGRAÇÃO ---
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
                # --- INÍCIO DA INTEGRAÇÃO DA IMAGEM ---
                print(f"\nIniciando busca de imagem para: {lab_atual['nome']}")
                # chama o script
                caminho_imagem_local = encontrar_imagem_para_lab(lab_atual['nome'], PASTA_IMAGENS_LABS)
                
                if caminho_imagem_local:
                    # Solução 2: Imagem baixada!
                    # Precisamos salvar o caminho relativo ao CSV (que está em ../Labs)
                    lab_atual['caminho_imagem'] = os.path.join("..", "images", "labs", os.path.basename(caminho_imagem_local))
                else:
                    # Solução 1: Placeholder
                    lab_atual['caminho_imagem'] = CAMINHO_PLACEHOLDER
                
                time.sleep(1.5) 
                # --- FIM DA INTEGRAÇÃO ---
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
    if labs_fga_final:
        # Salva no CSV de saída
        with open(csv_saida, 'w', newline='', encoding='utf-8') as f:
            campos = ['nome', 'coordenador', 'contato', 'descricao', 'caminho_imagem']
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(labs_fga_final)

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
