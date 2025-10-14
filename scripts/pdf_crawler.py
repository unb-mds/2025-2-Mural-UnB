import requests  # baixa o HTML
from bs4 import BeautifulSoup  # organiza o HTML em python
import urllib.parse  # manipula URLs

url_alvo = "http://pesquisa.unb.br/infraestrutura-de-pesquisa?menu=788" # o link do laboratório

print(f"Acessando a pagina: {url_alvo}...") 

try:
    # 1. Fazer a requisição HTTP para baixar o HTML
    response = requests.get(url_alvo, timeout=20)  #response = a caixa com tudo que veio da url, pode ser mais ou menos que o HTML puro
    response.raise_for_status()  # deu certo ou não?
    
    # 2. Parsear (organizar) o HTML usando BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser') # o .content é o conteúdo bruto HTML, html.parser é o tradutor, o BeautifulSoup organiza de forma legível em python
    
    # 3. Buscar TODAS as tags <a> (links) que possuem o atributo href
    print("Procurando PDFs na pagina...")
    print("-" * 60)
    
    todos_links = soup.find_all('a', href=True)
    print(f"Total de links encontrados na pagina: {len(todos_links)}\n")
    
    # 4. Filtrar apenas os links que terminam com .pdf
    links_pdf = []
    urls_ja_adicionadas = set()  # para evitar duplicatas
    
    for link in todos_links:
        href = link['href']  # pega o valor do atributo href
        
        # Verifica se o link termina com .pdf
        if href.endswith('.pdf'):
            # 5. Converter links relativos em URLs absolutas
            url_completa = urllib.parse.urljoin(url_alvo, href)
            
            # Evita adicionar o mesmo PDF duas vezes
            if url_completa not in urls_ja_adicionadas:
                urls_ja_adicionadas.add(url_completa)
                
                # Pega o texto dentro da tag <a>texto</a>
                texto_link = link.get_text(strip=True)
                
                links_pdf.append({
                    'url': url_completa,
                    'texto': texto_link if texto_link else 'PDF sem descricao'
                })
    
    # 6. Imprimir os resultados
    print("=" * 60)
    print(f"TOTAL DE PDFs ENCONTRADOS: {len(links_pdf)}")
    print("=" * 60)
    
    if links_pdf:
        print("\nLISTA DE URLs DE PDF:")
        print("-" * 60)
        for i, pdf in enumerate(links_pdf, 1):
            print(f"\n[{i}] {pdf['texto']}")
            print(f"    URL: {pdf['url']}")
        print("\n" + "=" * 60)
    else:
        print("Nenhum PDF encontrado nesta página.")
    
    
except requests.exceptions.Timeout:
    print("\n✗ ERRO: A página demorou muito para responder (timeout).")
    exit(1)
except requests.exceptions.ConnectionError:
    print("\n✗ ERRO: Não foi possível conectar ao servidor.")
    exit(1)
except requests.exceptions.HTTPError as e:
    print(f"\n✗ ERRO HTTP: {e}")
    exit(1)
except requests.exceptions.RequestException as motivo: # categoria de todos os erros que podem vir na biblioteca requests, guarde a info no 'motivo'
    print(f"\n✗ Erro ao acessar a página: {motivo}")
    exit(1)

