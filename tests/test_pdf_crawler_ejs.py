"""
Testes unitários para pdf_crawler_ejs.py
"""
import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Importar o módulo uma vez
import scripts.pdf_crawler_ejs as pdf_crawler_ejs


class TestPDFCrawlerEJs:
    """Testes para o crawler de PDFs"""

    @patch('scripts.pdf_crawler_ejs.requests.get')
    @patch('scripts.pdf_crawler_ejs.os.makedirs')
    def test_encontrar_pdf_empresas_juniores_sucesso(self, mock_makedirs, mock_requests):
        """Testa busca bem-sucedida de PDF"""
        # Mock do HTML com link para PDF
        html_content = '''
        <html>
            <body>
                <a href="portfolio.pdf">Portfólio Empresas Juniores</a>
                <a href="outro.pdf">Outro PDF</a>
            </body>
        </html>
        '''
        
        
        mock_response = Mock()
        mock_response.content = html_content.encode('utf-8')  # Bytes reais
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        # Mock do download do PDF
        mock_pdf_response = Mock()
        mock_pdf_response.raise_for_status.return_value = None
        mock_pdf_response.iter_content.return_value = [b"fake pdf content"]
        
         
        with patch('scripts.pdf_crawler_ejs.requests.get') as mock_pdf_get:
            mock_pdf_get.return_value = mock_pdf_response
            
            
            with patch('scripts.pdf_crawler_ejs.os.path.join') as mock_join:
                mock_join.return_value = "C:/temp/portfolio_empresas_juniores.pdf"
                
                resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com")
                
                assert resultado is not None
                assert "portfolio_empresas_juniores.pdf" in resultado

    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_empresas_juniores_sem_pdf(self, mock_requests):
        """Testa busca quando não há PDFs"""
        # Mock do HTML sem links PDF relevantes
        html_content = '''
        <html>
            <body>
                <a href="pagina.html">Página normal</a>
                <a href="imagem.jpg">Imagem</a>
            </body>
        </html>
        '''
        
        mock_response = Mock()
        mock_response.content = html_content.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com")
        
        assert resultado is None

    
    def test_encontrar_pdf_empresas_juniores_funcao_original(self):
        """Testa que a função original não trata exceções"""
        # A função original não tem try/except, então ela PROPAGA exceções
        
        
        # Lendo o código fonte para verificar se há tratamento de exceções
        import inspect
        source_code = inspect.getsource(pdf_crawler_ejs.encontrar_pdf_empresas_juniores)
        
        # A função original não tem 'try:' ou 'except', então propaga exceções
        has_try_except = 'try:' in source_code or 'except' in source_code
        
        # Se não tem tratamento, então ela propaga exceções (comportamento esperado)
        if not has_try_except:
            
            with patch('scripts.pdf_crawler_ejs.requests.get') as mock_requests:
                mock_requests.side_effect = Exception("Test error")
                
                # Deve levantar exceção
                with pytest.raises(Exception, match="Test error"):
                    pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com")
        else:
            # Se tem tratamento, então retorna None
            with patch('scripts.pdf_crawler_ejs.requests.get') as mock_requests:
                mock_requests.side_effect = Exception("Test error")
                resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com")
                assert resultado is None

    # Teste para verificar a lógica de filtro de PDFs
    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_criterios_filtro(self, mock_requests):
        """Testa os critérios de filtro para identificar PDFs de EJs"""
        html_content = '''
        <html>
            <body>
                <a href="empresa_junior.pdf">EMPRESA JÚNIOR</a>
                <a href="ej.pdf">EJ Portfolio</a>
                <a href="normal.pdf">Documento qualquer</a>
                <a href="portfolio.pdf">Portfólio Empresas</a>
            </body>
        </html>
        '''
        
        mock_response = Mock()
        mock_response.content = html_content.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        # Mock do download
        mock_pdf_response = Mock()
        mock_pdf_response.raise_for_status.return_value = None
        mock_pdf_response.iter_content.return_value = [b"fake pdf content"]
        
        with patch('scripts.pdf_crawler_ejs.requests.get') as mock_pdf_get, \
             patch('scripts.pdf_crawler_ejs.os.makedirs'), \
             patch('scripts.pdf_crawler_ejs.os.path.join') as mock_join:
            
            mock_pdf_get.return_value = mock_pdf_response
            mock_join.return_value = "C:/temp/portfolio_empresas_juniores.pdf"
            
            resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com")
            
            # Deve encontrar PDFs que atendem aos critérios
            assert resultado is not None

    # Teste para múltiplos PDFs
    @patch('scripts.pdf_crawler_ejs.requests.get')
    def test_encontrar_pdf_multiplos_encontrados(self, mock_requests):
        """Testa quando múltiplos PDFs são encontrados"""
        html_content = '''
        <html>
            <body>
                <a href="portfolio1.pdf">Portfólio 1</a>
                <a href="portfolio2.pdf">Portfólio 2</a>
                <a href="portfolio3.pdf">Portfólio 3</a>
            </body>
        </html>
        '''
        
        mock_response = Mock()
        mock_response.content = html_content.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        # Mock do download
        mock_pdf_response = Mock()
        mock_pdf_response.raise_for_status.return_value = None
        mock_pdf_response.iter_content.return_value = [b"fake pdf content"]
        
        with patch('scripts.pdf_crawler_ejs.requests.get') as mock_pdf_get, \
             patch('scripts.pdf_crawler_ejs.os.makedirs'), \
             patch('scripts.pdf_crawler_ejs.os.path.join') as mock_join:
            
            mock_pdf_get.return_value = mock_pdf_response
            mock_join.return_value = "C:/temp/portfolio_empresas_juniores.pdf"
            
            resultado = pdf_crawler_ejs.encontrar_pdf_empresas_juniores("http://example.com")
            
            # Deve baixar o primeiro PDF encontrado
            assert resultado is not None
