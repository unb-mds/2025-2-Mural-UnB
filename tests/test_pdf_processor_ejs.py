"""
Testes unitários para pdf_processor_ejs.py
"""
import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
import sys


# Adiciona o caminho para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import scripts.pdf_processor_ejs as pdf_processor_ejs

class TestPDFProcessorEJs:
    """Testes para a classe PDFProcessorEJs"""

    def test_init(self):
        """Testa a inicialização da classe"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        assert processor.gemini_api_key == "test-api-key"
        assert processor.model is not None

    def test_limpar_texto(self):
        """Testa a limpeza de texto"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        # Texto com caracteres especiais
        texto_sujo = "Texto\u202fcom\xa0caracteres\u2013especiais\u2014problema"
        texto_limpo = processor.limpar_texto(texto_sujo)
        
        assert "\u202f" not in texto_limpo
        assert "\xa0" not in texto_limpo
        assert "\u2013" not in texto_limpo
        assert "\u2014" not in texto_limpo

    def test_limpar_texto_vazio(self):
        """Testa limpeza de texto vazio"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        assert processor.limpar_texto("") == ""
        assert processor.limpar_texto(None) is None

    def test_juntar_palavras_hifenizadas(self):
        """Testa a junção de palavras hifenizadas"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        texto_hifenizado = "Esta é uma pala-\n vra hifenizada."
        texto_corrigido = processor.juntar_palavras_hifenizadas(texto_hifenizado)
        
        assert "pala-\n vra" not in texto_corrigido
        assert "palavra" in texto_corrigido

    def test_juntar_palavras_hifenizadas_vazio(self):
        """Testa junção de palavras hifenizadas com texto vazio"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        assert processor.juntar_palavras_hifenizadas("") == ""
        assert processor.juntar_palavras_hifenizadas(None) is None

    def test_criar_prompt_gemini(self):
        """Testa a criação do prompt para Gemini"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        texto_teste = "Texto de exemplo para teste"
        prompt = processor.criar_prompt_gemini(texto_teste, "Página 1")
        
        assert "ANALISE O TEXTO E EXTRAIA INFORMAÇÕES SOBRE EMPRESAS JUNIORES" in prompt
        assert texto_teste in prompt
        assert "array JSON válido" in prompt

    def test_limpar_e_corrigir_json(self):
        """Testa a limpeza e correção de JSON"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        # JSON com markdown
        json_sujo = "```json\n[{\"Nome\": \"Teste\"}]\n```"
        json_limpo = processor.limpar_e_corrigir_json(json_sujo)
        
        assert "```" not in json_limpo
        assert json_limpo.strip() == '[{"Nome": "Teste"}]'

    def test_limpar_e_corrigir_json_sem_array(self):
        """Testa correção de JSON que não começa com array"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        json_sem_array = '{"Nome": "Teste"}'
        json_corrigido = processor.limpar_e_corrigir_json(json_sem_array)
        
        assert json_corrigido.strip().startswith('[')
        assert json_corrigido.strip().endswith(']')

    def test_corrigir_json(self):
        """Testa correção agressiva de JSON malformado"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        json_malformado = "Texto antes {\"Nome\": 'Teste'} texto depois"
        json_corrigido = processor.corrigir_json(json_malformado)
        
        assert "Texto antes" not in json_corrigido
        assert "texto depois" not in json_corrigido
        assert "'Teste'" not in json_corrigido  # Aspas simples devem ser substituídas

    def test_empresa_duplicada(self):
        """Testa detecção de empresas duplicadas"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        empresas_existentes = [
            {"Nome": "Empresa A", "Cursos": "Engenharia"},
            {"Nome": "Empresa B", "Cursos": "Computação"}
        ]
        
        # Empresa duplicada
        nova_duplicada = {"Nome": "Empresa A", "Cursos": "Outro Curso"}
        assert processor.empresa_duplicada(nova_duplicada, empresas_existentes) is True
        
        # Empresa nova
        nova_empresa = {"Nome": "Empresa C", "Cursos": "Medicina"}
        assert processor.empresa_duplicada(nova_empresa, empresas_existentes) is False

    def test_empresa_duplicada_sem_nome(self):
        """Testa detecção de empresas sem nome"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        empresas_existentes = [{"Nome": "Empresa A"}]
        empresa_sem_nome = {"Cursos": "Engenharia"}
        
        assert processor.empresa_duplicada(empresa_sem_nome, empresas_existentes) is False

    @patch('pdf_processor_ejs.requests.get')
    def test_baixar_pdf_direto_sucesso(self, mock_requests):
        """Testa download bem-sucedido de PDF"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        # Mock da resposta
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b"pdf content"]
        mock_requests.return_value = mock_response
        
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho_saida = os.path.join(temp_dir, "test.pdf")
            resultado = processor.baixar_pdf_direto("http://example.com/test.pdf", caminho_saida)
            
            assert resultado == caminho_saida
            assert os.path.exists(caminho_saida)

    @patch('pdf_processor_ejs.requests.get')
    def test_baixar_pdf_direto_erro(self, mock_requests):
        """Testa download de PDF com erro"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        mock_requests.side_effect = Exception("Erro de conexão")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho_saida = os.path.join(temp_dir, "test.pdf")
            
            with pytest.raises(Exception):
                processor.baixar_pdf_direto("http://example.com/test.pdf", caminho_saida)

    @patch('pdf_processor_ejs.pdfplumber.open')
    def test_extrair_texto_por_pagina(self, mock_pdfplumber):
        """Testa extração de texto por página"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        # Mock das páginas
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Texto da página 1"
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Texto da página 2"
        
        mock_pdf = Mock()
        mock_pdf.pages = [mock_page1, mock_page2]
        mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
        
        with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
            resultado = processor.extrair_texto_por_pagina(temp_file.name)
            
            assert len(resultado) == 2
            assert resultado[0]['texto'] == "Texto da página 1"
            assert resultado[1]['texto'] == "Texto da página 2"

    @patch('pdf_processor_ejs.pdfplumber.open')
    def test_extrair_texto_por_pagina_vazia(self, mock_pdfplumber):
        """Testa extração de texto de página vazia"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        mock_page = Mock()
        mock_page.extract_text.return_value = ""  # Página vazia
        
        mock_pdf = Mock()
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
        
        with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
            resultado = processor.extrair_texto_por_pagina(temp_file.name)
            
            assert len(resultado) == 0

    def test_salvar_json(self):
        """Testa salvamento de JSON"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        dados_teste = [
            {"Nome": "Empresa A", "Cursos": "Engenharia"},
            {"Nome": "Empresa B", "Cursos": "Computação"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            try:
                processor.salvar_json(dados_teste, temp_file.name)
                
                # Verifica se o arquivo foi criado e tem conteúdo
                assert os.path.exists(temp_file.name)
                
                with open(temp_file.name, 'r', encoding='utf-8') as f:
                    dados_salvos = json.load(f)
                
                assert len(dados_salvos) == 2
                assert dados_salvos[0]['Nome'] == "Empresa A"
            finally:
                os.unlink(temp_file.name)

    @patch('pdf_processor_ejs.fitz.open')
    def test_extrair_imagens_pdf(self, mock_fitz):
        """Testa extração de imagens do PDF"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        # Mock do documento PDF
        mock_doc = Mock()
        mock_page = Mock()
        mock_page.get_images.return_value = [(1,)]
        
        mock_image = Mock()
        mock_image.extract_image.return_value = {
            "image": b"fake image data",
            "ext": "png"
        }
        mock_page.get_image.return_value = mock_image
        
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz.return_value = mock_doc
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
                resultado = processor.extrair_imagens_pdf(temp_file.name, temp_dir)
                
                # Verifica se a função retornou uma lista
                assert isinstance(resultado, list)

    @patch.object(pdf_processor_ejs.PDFProcessorEJs, 'extrair_informacoes_gemini')
    @patch.object(pdf_processor_ejs.PDFProcessorEJs, 'extrair_texto_por_pagina')
    def test_processar_pdf_paginado(self, mock_extrair_texto, mock_extrair_gemini):
        """Testa processamento paginado do PDF"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        # Mock dos dados de texto
        mock_extrair_texto.return_value = [
            {"numero_pagina": 1, "texto": "Texto página 1", "contagem_caracteres": 100},
            {"numero_pagina": 2, "texto": "Texto página 2", "contagem_caracteres": 100}
        ]
        
        # Mock da resposta do Gemini
        mock_extrair_gemini.return_value = [
            {"Nome": "Empresa Teste", "Cursos": "Engenharia"}
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, "test.pdf")
            json_path = os.path.join(temp_dir, "output.json")
            
            # Cria arquivo PDF vazio para o teste
            with open(pdf_path, 'w') as f:
                f.write("fake pdf content")
            
            resultado = processor.processar_pdf_paginado(pdf_path, json_path)
            
            assert len(resultado) > 0
            assert resultado[0]['id'] is not None  # IDs devem ser gerados

    @patch('google.generativeai.GenerativeModel')
    def test_extrair_informacoes_gemini_sucesso(self, mock_model):
        """Testa extração bem-sucedida com Gemini"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        # Mock da resposta do Gemini
        mock_response = Mock()
        mock_response.text = '[{"Nome": "Empresa Teste", "Cursos": "Engenharia"}]'
        mock_model.return_value.generate_content.return_value = mock_response
        
        resultado = processor.extrair_informacoes_gemini("Texto de teste")
        
        assert len(resultado) == 1
        assert resultado[0]['Nome'] == "Empresa Teste"

    @patch('google.generativeai.GenerativeModel')
    def test_extrair_informacoes_gemini_json_invalido(self, mock_model):
        """Testa extração com JSON inválido do Gemini"""
        processor = pdf_processor_ejs.PDFProcessorEJs("test-api-key")
        
        # Mock da resposta com JSON inválido
        mock_response = Mock()
        mock_response.text = 'JSON inválido { Nome: "Empresa" }'
        mock_model.return_value.generate_content.return_value = mock_response
        
        resultado = processor.extrair_informacoes_gemini("Texto de teste")
        
        # Deve retornar lista vazia quando não consegue processar JSON
        assert resultado == []