"""
Rastreia páginas para localizar e baixar o PDF das Empresas Juniores.
Detecta links PDF relevantes e salva o Portfólio em `data/EJs`.
"""
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import warnings

# Suprimir avisos de SSL (necessário para alguns sites da UnB)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def encontrar_pdf_empresas_juniores(url_alvo):
    """
    Encontra e baixa o PDF de empresas juniores
    """
    print(f"Acessando a pagina: {url_alvo}...") 

    try:
        # Headers para simular um navegador (alguns sites bloqueiam bots)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
        }
        
        # 1. Fazer a requisição HTTP para baixar o HTML
        # Nota: verify=False desabilita verificação SSL (necessário para alguns sites da UnB)
        response = requests.get(url_alvo, headers=headers, timeout=20, allow_redirects=True, verify=False)
        response.raise_for_status()
        
        # 2. Parsear o HTML usando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 3. Buscar TODAS as tags <a> (links)
        print("Procurando PDFs na pagina...")
        print("-" * 60)
        
        todos_links = soup.find_all('a', href=True)
        print(f"Total de links encontrados na pagina: {len(todos_links)}\n")
        
        # 4. Filtrar PDFs relacionados a empresas juniores
        links_pdf = []
        urls_ja_adicionadas = set()
        
        for link in todos_links:
            href = link['href']
            texto_link = link.get_text(strip=True)
            
            # Critérios para identificar PDF de empresas junior
            criterios_pdf_ej = [
                href.endswith('.pdf'),
                any(termo in texto_link.upper() for termo in ['EMPRESA', 'JÚNIOR', 'JUNIOR', 'EJ', 'PORTFÓLIO']),
                any(termo in href.upper() for termo in ['EMPRESA', 'JUNIOR', 'EJ', 'PORTFOLIO'])
            ]
            
            if all(criterios_pdf_ej[:1]) and any(criterios_pdf_ej[1:]):
                # Converter links relativos em URLs absolutas
                url_completa = urllib.parse.urljoin(url_alvo, href)
                
                if url_completa not in urls_ja_adicionadas:
                    urls_ja_adicionadas.add(url_completa)
                    
                    links_pdf.append({
                        'url': url_completa,
                        'texto': texto_link if texto_link else 'PDF Empresas Juniores'
                    })
        
        # 5. Imprimir resultados
        print("=" * 60)
        print(f"TOTAL DE PDFs DE EJs ENCONTRADOS: {len(links_pdf)}")
        print("=" * 60)
        
        if links_pdf:
            print("\nLISTA DE URLs DE PDF:")
            print("-" * 60)
            for i, pdf in enumerate(links_pdf, 1):
                print(f"\n[{i}] {pdf['texto']}")
                print(f"    URL: {pdf['url']}")
            print("\n" + "=" * 60)
            
            # 6. Baixar o primeiro PDF encontrado
            pdf_principal = links_pdf[0]
            print(f"\nBaixando o PDF: {pdf_principal['texto']}")
            print(f"URL: {pdf_principal['url']}")
            
            # Define o caminho onde salvar
            pasta_saida = os.path.join(os.path.dirname(__file__), "..", "data", "EJs")
            os.makedirs(pasta_saida, exist_ok=True)
            
            nome_arquivo = "portfolio_empresas_juniores.pdf"
            caminho_completo = os.path.join(pasta_saida, nome_arquivo)
            
            # Baixa o PDF
            response_pdf = requests.get(pdf_principal['url'], headers=headers, stream=True, timeout=30, allow_redirects=True, verify=False)
            response_pdf.raise_for_status()
            
            # Salva o arquivo
            with open(caminho_completo, 'wb') as arquivo:
                for pedaco in response_pdf.iter_content(chunk_size=8192):
                    arquivo.write(pedaco)
            
            print(f"\n PDF baixado com sucesso: {caminho_completo}")
            print("=" * 60)
            
            return caminho_completo
        else:
            print("Nenhum PDF de empresas juniores encontrado.")
            return None
        
    except requests.exceptions.Timeout:
        print("\n ERRO: A página demorou muito para responder (timeout).")
        print(f"URL tentada: {url_alvo}")
        return None
    except requests.exceptions.ConnectionError as e:
        print("\n ERRO: Não foi possível conectar ao servidor.")
        print(f"URL tentada: {url_alvo}")
        print(f"Detalhes: {str(e)}")
        print("\nPossíveis causas:")
        print("  - URL incorreta ou site fora do ar")
        print("  - Firewall ou proxy bloqueando a conexão")
        print("  - Problema de DNS")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"\n ERRO HTTP: {e}")
        print(f"URL tentada: {url_alvo}")
        return None
    except requests.exceptions.RequestException as motivo:
        print(f"\n Erro ao acessar a página: {motivo}")
        print(f"URL tentada: {url_alvo}")
        return None

if __name__ == "__main__":
    # URL pra exemplo - substituir dps pela URL real do portfólio de EJ
    url_ejs = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
    pdf_path = encontrar_pdf_empresas_juniores(url_ejs)
    
    if pdf_path:
        print(f"\nPDF disponível em: {pdf_path}")
    else:

        print("\nNão foi possível obter o PDF.")
