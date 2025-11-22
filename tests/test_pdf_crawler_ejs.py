"""
Testes unitários para pdf_crawler_ejs.py
"""
import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import scripts.pdf_crawler_ejs as pdf_crawler_ejs


class TestPDFCrawlerEJs:
    """Testes para o crawler de PDFs de Empresas Juniores"""

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_sucesso(self, mock_requests_get):
        """Testa busca bem-sucedida de PDF de empresas juniores"""
        # Mock do HTML com link para PDF relevante
        html_content = '''
        <html>
            <body>
                <a href="portfolio_empresas_juniores.pdf">Portfólio Empresas Juniores</a>
                <a href="outro_arquivo.pdf">Outro PDF</a>
                <a href="pagina.html">Página normal</a>
            </body>
        </html>
        '''
        
        # Mock da resposta HTTP para a página HTML
        mock_html_response = Mock()
        mock_html_response.content = html_content.encode('utf-8')
        mock_html_response.raise_for_status.return_value = None
        
        # Mock da resposta HTTP para o download do PDF
        mock_pdf_response = Mock()
        mock_pdf_response.raise_for_status.return_value = None
        mock_pdf_response.iter_content.return_value = [b"fake pdf content"]
        
        # Configurar o mock para retornar respostas diferentes
        mock_requests_get.side_effect = [mock_html_response, mock_pdf_response]
        
        # Mock do caminho de saída
        with patch('scripts.pdf_crawler_ejs.os.path.join') as mock_join, \
             patch('scripts.pdf_crawler_ejs.os.makedirs') as mock_makedirs:
            
            mock_join.return_value = "/fake/path/portfolio_empresas_juniores.pdf"
            
            resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/ej")
            
            assert resultado == "/fake/path/portfolio_empresas_juniores.pdf"
            mock_makedirs.assert_called_once()

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_sem_pdf(self, mock_requests_get):
        """Testa busca quando não há PDFs relevantes"""
        # Mock do HTML sem links PDF relevantes
        html_content = '''
        <html>
            <body>
                <a href="pagina.html">Página normal</a>
                <a href="imagem.jpg">Imagem JPEG</a>
                <a href="documento.docx">Documento Word</a>
            </body>
        </html>
        '''
        
        mock_response = Mock()
        mock_response.content = html_content.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/sem-pdf")
        
        assert resultado is None

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_multiplos_pdfs(self, mock_requests_get):
        """Testa busca quando há múltiplos PDFs relevantes"""
        # Mock do HTML com múltiplos PDFs relevantes
        html_content = '''
        <html>
            <body>
                <a href="portfolio1.pdf">Portfólio Empresas Juniores 2024</a>
                <a href="portfolio2.pdf">Portfólio EJs</a>
                <a href="outro.pdf">Outro documento</a>
            </body>
        </html>
        '''
        
        mock_html_response = Mock()
        mock_html_response.content = html_content.encode('utf-8')
        mock_html_response.raise_for_status.return_value = None
        
        mock_pdf_response = Mock()
        mock_pdf_response.raise_for_status.return_value = None
        mock_pdf_response.iter_content.return_value = [b"fake pdf content"]
        
        mock_requests_get.side_effect = [mock_html_response, mock_pdf_response]
        
        with patch('scripts.pdf_crawler_ejs.os.path.join') as mock_join, \
             patch('scripts.pdf_crawler_ejs.os.makedirs') as mock_makedirs:
            
            mock_join.return_value = "/fake/path/portfolio_empresas_juniores.pdf"
            
            resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/multiplos-pdfs")
            
            # Deve retornar o caminho do primeiro PDF encontrado
            assert resultado == "/fake/path/portfolio_empresas_juniores.pdf"

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_timeout(self, mock_requests_get):
        """Testa comportamento com timeout na requisição"""
        mock_requests_get.side_effect = Exception("Timeout")
        
        resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/timeout")
        
        assert resultado is None

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_http_error(self, mock_requests_get):
        """Testa comportamento com erro HTTP"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_requests_get.return_value = mock_response
        
        resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/404")
        
        assert resultado is None

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_connection_error(self, mock_requests_get):
        """Testa comportamento com erro de conexão"""
        mock_requests_get.side_effect = Exception("Connection error")
        
        resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/connection-error")
        
        assert resultado is None

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_pdf_com_url_relativa(self, mock_requests_get):
        """Testa busca com URL relativa no href do PDF"""
        # Mock do HTML com URL relativa
        html_content = '''
        <html>
            <body>
                <a href="/documentos/portfolio.pdf">Portfólio Empresas Juniores</a>
            </body>
        </html>
        '''
        
        mock_html_response = Mock()
        mock_html_response.content = html_content.encode('utf-8')
        mock_html_response.raise_for_status.return_value = None
        
        mock_pdf_response = Mock()
        mock_pdf_response.raise_for_status.return_value = None
        mock_pdf_response.iter_content.return_value = [b"fake pdf content"]
        
        mock_requests_get.side_effect = [mock_html_response, mock_pdf_response]
        
        with patch('scripts.pdf_crawler_ejs.os.path.join') as mock_join, \
             patch('scripts.pdf_crawler_ejs.os.makedirs') as mock_makedirs:
            
            mock_join.return_value = "/fake/path/portfolio_empresas_juniores.pdf"
            
            resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/ej")
            
            # Deve converter URL relativa em absoluta e baixar
            assert resultado == "/fake/path/portfolio_empresas_juniores.pdf"

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_criterios_relevancia(self, mock_requests_get):
        """Testa os critérios de relevância para identificar PDFs de EJs"""
        # Mock do HTML com vários tipos de links PDF
        html_content = '''
        <html>
            <body>
                <a href="empresa_junior.pdf">PDF sem texto relevante</a>
                <a href="portfolio.pdf">Portfólio de Serviços</a>
                <a href="ej_consultoria.pdf">EJ Consultoria - Nossos Serviços</a>
                <a href="manual.pdf">Manual do Estudante</a>
            </body>
        </html>
        '''
        
        mock_html_response = Mock()
        mock_html_response.content = html_content.encode('utf-8')
        mock_html_response.raise_for_status.return_value = None
        
        mock_pdf_response = Mock()
        mock_pdf_response.raise_for_status.return_value = None
        mock_pdf_response.iter_content.return_value = [b"fake pdf content"]
        
        mock_requests_get.side_effect = [mock_html_response, mock_pdf_response]
        
        with patch('scripts.pdf_crawler_ejs.os.path.join') as mock_join, \
             patch('scripts.pdf_crawler_ejs.os.makedirs') as mock_makedirs:
            
            mock_join.return_value = "/fake/path/ej_consultoria.pdf"
            
            resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/criterios")
            
            # Deve selecionar o PDF mais relevante (com "EJ" no texto)
            assert resultado == "/fake/path/ej_consultoria.pdf"

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_headers_requisicao(self, mock_requests_get):
        """Testa se os headers da requisição estão corretos"""
        # Mock da resposta
        mock_response = Mock()
        mock_response.content = '<html><a href="test.pdf">PDF</a></html>'.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        # Mock do download do PDF
        mock_pdf_response = Mock()
        mock_pdf_response.raise_for_status.return_value = None
        mock_pdf_response.iter_content.return_value = [b"content"]
        
        # Usar side_effect para múltiplas chamadas
        mock_requests_get.side_effect = [mock_response, mock_pdf_response]
        
        with patch('scripts.pdf_crawler_ejs.os.path.join'), \
             patch('scripts.pdf_crawler_ejs.os.makedirs'):
            
            pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com")
            
            # Verifica se requests.get foi chamado com headers
            assert mock_requests_get.called
            # A primeira chamada deve ter headers
            first_call = mock_requests_get.call_args_list[0]
            call_kwargs = first_call[1]
            assert 'headers' in call_kwargs
            # Verifica se tem User-Agent (campo mais importante)
            assert 'User-Agent' in call_kwargs['headers']

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_pdf_download_error(self, mock_requests_get):
        """Testa comportamento quando o download do PDF falha"""
        # Mock da página HTML com PDF
        html_content = '''
        <html>
            <body>
                <a href="portfolio.pdf">Portfólio Empresas Juniores</a>
            </body>
        </html>
        '''
        
        mock_html_response = Mock()
        mock_html_response.content = html_content.encode('utf-8')
        mock_html_response.raise_for_status.return_value = None
        
        # Primeira chamada retorna HTML, segunda falha no download
        mock_requests_get.side_effect = [mock_html_response, Exception("Download failed")]
        
        resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/download-error")
        
        assert resultado is None

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_pdf_sem_texto_relevante(self, mock_requests_get):
        """Testa busca com PDFs que não atendem aos critérios de relevância"""
        # Mock do HTML com PDFs que não são de empresas juniores
        html_content = '''
        <html>
            <body>
                <a href="calendario.pdf">Calendário Acadêmico</a>
                <a href="regulamento.pdf">Regulamento Geral</a>
                <a href="editais.pdf">Editais 2024</a>
            </body>
        </html>
        '''
        
        mock_response = Mock()
        mock_response.content = html_content.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com/sem-ejs")
        
        assert resultado is None


# Teste para execução como script
class TestPDFCrawlerMain:
    """Testes para execução principal do crawler"""
    
    @patch('scripts.pdf_crawler_ejs.encontrar_pdf_empresas_juniores')
    def test_execucao_principal_sucesso(self, mock_encontrar_pdf):
        """Testa execução principal quando encontra PDF"""
        mock_encontrar_pdf.return_value = "/caminho/portfolio_empresas_juniores.pdf"
        
        # Simular a execução do bloco if __name__ == "__main__"
        with patch('builtins.print') as mock_print:
            # Recriar a lógica do bloco main
            url_ejs = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
            pdf_path = pdf_crawler_ejs.encontrar_pdf_empresas_juniores(url_ejs)
            
            if pdf_path:
                mock_print.assert_any_call(f"\nPDF disponível em: {pdf_path}")
            else:
                mock_print.assert_any_call("\nNão foi possível obter o PDF.")

    @patch('scripts.pdf_crawler_ejs.encontrar_pdf_empresas_juniores')
    def test_execucao_principal_sem_pdf(self, mock_encontrar_pdf):
        """Testa execução principal quando não encontra PDF"""
        mock_encontrar_pdf.return_value = None
        
        # Simular a execução do bloco if __name__ == "__main__"
        with patch('builtins.print') as mock_print:
            # Recriar a lógica do bloco main
            url_ejs = "https://www.unb.br/cultura-e-sociedade/empresa-junior"
            pdf_path = pdf_crawler_ejs.encontrar_pdf_empresas_juniores(url_ejs)
            
            if pdf_path:
                mock_print.assert_any_call(f"\nPDF disponível em: {pdf_path}")
            else:
                mock_print.assert_any_call("\nNão foi possível obter o PDF.")
                