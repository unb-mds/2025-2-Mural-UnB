"""
Busca e baixa o PDF do portfólio de infraestrutura no site da UnB.
Salva o arquivo em `data/Labs` para processamento posterior.
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

url_alvo = "http://pesquisa.unb.br/infraestrutura-de-pesquisa?menu=788"

#
# 1. Toda a lógica agora está dentro de uma função main()
#
def main():
    print(f"Acessando a pagina: {url_alvo}...")

    try:
        # Fazer a requisição HTTP para baixar o HTML
        response = requests.get(url_alvo, timeout=20)
        response.raise_for_status()

        # Parsear (organizar) o HTML usando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar TODAS as tags <a> (links) que possuem o atributo href
        print("Procurando PDFs na pagina...")
        print("-" * 60)

        todos_links = soup.find_all('a', href=True)
        print(f"Total de links encontrados na pagina: {len(todos_links)}\n")

        # Filtrar apenas o PDF do Portfólio de Infraestrutura
        links_pdf = []
        urls_ja_adicionadas = set()

        for link in todos_links:
            href = link.get('href')
            texto_link = link.get_text(strip=True)

            # Verifica se o link termina com .pdf E contém "InfraPesquisa" ou "Portfólio"
            if href.endswith('.pdf') and ('InfraPesquisa' in href or 'Infraestrutura' in href):
                # Converter links relativos em URLs absolutas
                url_completa = urllib.parse.urljoin(url_alvo, href)
                
                if url_completa not in urls_ja_adicionadas:
                    urls_ja_adicionadas.add(url_completa)
                    
                    links_pdf.append({
                        'url': url_completa,
                        'texto': texto_link if texto_link else 'PDF sem descricao'
                    })
                    
        
        # Imprimir os resultados
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
            
            # Baixar o primeiro PDF encontrado (Portfólio de Infraestrutura)
            if links_pdf:
                pdf_principal = links_pdf[0]
                print(f"\nBaixando o PDF: {pdf_principal['texto']}")
                print(f"URL: {pdf_principal['url']}")
                
                # Define o caminho onde salvar
                pasta_saida = os.path.join(os.path.dirname(__file__), "..", "data", "Labs")
                os.makedirs(pasta_saida, exist_ok=True)
                
                nome_arquivo = "Portfolio_Infraestrutura_UnB.pdf"
                caminho_completo = os.path.join(pasta_saida, nome_arquivo)
                
                # Baixa o PDF
                response_pdf = requests.get(pdf_principal['url'], stream=True, timeout=30)
                response_pdf.raise_for_status()
                
                # Salva o arquivo
                with open(caminho_completo, 'wb') as arquivo:
                    for pedaco in response_pdf.iter_content(chunk_size=8192):
                        arquivo.write(pedaco)
                
                # Mostra informações
                print("\n   PDF baixado com sucesso!")
                print("=" * 60)
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
    except requests.exceptions.RequestException as motivo:
        print(f"\n✗ Erro ao acessar a página: {motivo}")
        exit(1)

#
# 2. Este bloco garante que main() só é chamado quando
#    o script é executado diretamente (e não quando é importado)
#
if __name__ == "__main__":
    main()