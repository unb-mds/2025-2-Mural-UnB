import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

def encontrar_pdf_empresas_juniores(url_alvo):
    """
    Encontra e baixa o PDF de empresas juniores
    """
    print(f"Acessando a pagina: {url_alvo}...") 

    try:
        # 1. Fazer a requisição HTTP para baixar o HTML
        response = requests.get(url_alvo, timeout=20)
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
            
            # Critérios para identificar PDF de empresas juniores
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
            
            nome_arquivo = "Portfolio_Empresas_Juniores_UnB.pdf"
            caminho_completo = os.path.join(pasta_saida, nome_arquivo)
            
            # Baixa o PDF
            response_pdf = requests.get(pdf_principal['url'], stream=True, timeout=30)
            response_pdf.raise_for_status()
            
            # Salva o arquivo
            with open(caminho_completo, 'wb') as arquivo:
                for pedaco in response_pdf.iter_content(chunk_size=8192):
                    arquivo.write(pedaco)
            
            print(f"\n✓ PDF baixado com sucesso: {caminho_completo}")
            print("=" * 60)
            
            return caminho_completo
        else:
            print("Nenhum PDF de empresas juniores encontrado.")
            return None
        
    except requests.exceptions.Timeout:
        print("\n✗ ERRO: A página demorou muito para responder (timeout).")
        return None
    except requests.exceptions.ConnectionError:
        print("\n✗ ERRO: Não foi possível conectar ao servidor.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"\n✗ ERRO HTTP: {e}")
        return None
    except requests.exceptions.RequestException as motivo:
        print(f"\n✗ Erro ao acessar a página: {motivo}")
        return None

if __name__ == "__main__":
    # URL pra exemplo - substituir dps pela URL real do portfólio de EJs
    url_ejs = "http://exemplo.com/ejuniores"
    pdf_path = encontrar_pdf_empresas_juniores(url_ejs)
    
    if pdf_path:
        print(f"\nPDF disponível em: {pdf_path}")
    else:
        print("\nNão foi possível obter o PDF.")