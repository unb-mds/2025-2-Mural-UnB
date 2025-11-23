import pytest
import os
import json
import tempfile
from unittest.mock import Mock, patch, ANY, MagicMock
import sys

# Adiciona o caminho para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from scripts.pdf_processor_ejs import PDFProcessorEJs

def test_pdf_processor_ejs_init(mocker):
    """Testa a inicialização do PDFProcessorEJs"""
    # Mock da configuração do Gemini para evitar erro de API key
    mock_configure = mocker.patch('pdf_processor_ejs.genai.configure')
    mock_model = mocker.patch('pdf_processor_ejs.genai.GenerativeModel')
    
    processor = PDFProcessorEJs("test-api-key")
    
    assert processor.gemini_api_key == "test-api-key"
    mock_configure.assert_called_once_with(api_key="test-api-key")
    mock_model.assert_called_once_with('gemini-2.5-flash-lite')

def test_limpar_texto():
    """Testa a limpeza de caracteres especiais"""
    processor = PDFProcessorEJs("test-api-key")
    
    texto_sujo = "Texto\u202fcom\xa0caracteres\u2013especiais\u2014problema"
    texto_limpo = processor.limpar_texto(texto_sujo)
    
    # Verifica que os caracteres especiais foram substituídos
    assert "\u202f" not in texto_limpo  # Narrow no-break space
    assert "\xa0" not in texto_limpo    # Non-breaking space
    assert "\u2013" not in texto_limpo  # En dash
    assert "\u2014" not in texto_limpo  # Em dash
    assert " " in texto_limpo  # Deve ter espaços normais
    assert "-" in texto_limpo  # Deve ter hífens normais

def test_limpar_texto_vazio():
    """Testa limpeza de texto vazio ou None"""
    processor = PDFProcessorEJs("test-api-key")
    
    assert processor.limpar_texto("") == ""
    assert processor.limpar_texto(None) is None

def test_juntar_palavras_hifenizadas():
    """Testa a junção de palavras hifenizadas"""
    processor = PDFProcessorEJs("test-api-key")
    
    texto_hifenizado = "Esta é uma pala-\n vra hifenizada."
    texto_corrigido = processor.juntar_palavras_hifenizadas(texto_hifenizado)
    
    assert "pala-\n vra" not in texto_corrigido
    assert "palavra" in texto_corrigido

def test_juntar_palavras_hifenizadas_vazio():
    """Testa junção de palavras hifenizadas com texto vazio"""
    processor = PDFProcessorEJs("test-api-key")
    
    assert processor.juntar_palavras_hifenizadas("") == ""
    assert processor.juntar_palavras_hifenizadas(None) is None

def test_criar_prompt_gemini():
    """Testa a criação do prompt para Gemini"""
    processor = PDFProcessorEJs("test-api-key")
    
    texto_teste = "Texto de exemplo para teste"
    prompt = processor.criar_prompt_gemini(texto_teste, "Página 1")
    
    assert "ANALISE O TEXTO E EXTRAIA INFORMAÇÕES SOBRE EMPRESAS JUNIORES" in prompt
    assert texto_teste in prompt
    assert "array JSON válido" in prompt
    assert "Nome" in prompt
    assert "Cursos" in prompt
    assert "Servicos" in prompt

def test_limpar_e_corrigir_json():
    """Testa a limpeza e correção de JSON"""
    processor = PDFProcessorEJs("test-api-key")
    
    # JSON com markdown
    json_sujo = "```json\n[{\"Nome\": \"Teste\"}]\n```"
    json_limpo = processor.limpar_e_corrigir_json(json_sujo)
    
    assert "```" not in json_limpo
    assert json_limpo.strip() == '[{"Nome": "Teste"}]'

def test_limpar_e_corrigir_json_sem_array():
    """Testa correção de JSON que não começa com array"""
    processor = PDFProcessorEJs("test-api-key")
    
    json_sem_array = '{"Nome": "Teste"}'
    json_corrigido = processor.limpar_e_corrigir_json(json_sem_array)
    
    assert json_corrigido.strip().startswith('[')
    assert json_corrigido.strip().endswith(']')

def test_corrigir_json():
    """Testa correção agressiva de JSON malformado"""
    processor = PDFProcessorEJs("test-api-key")
    
    json_malformado = "{\"Nome\": 'Teste'}"  # JSON mais simples
    json_corrigido = processor.corrigir_json(json_malformado)
    
    # Verifica que as aspas simples foram corrigidas
    assert "'Teste'" not in json_corrigido
    assert '"Teste"' in json_corrigido
    # Verifica que é um array
    assert json_corrigido.startswith('[')
    assert json_corrigido.endswith(']')

def test_empresa_duplicada():
    """Testa detecção de empresas duplicadas"""
    processor = PDFProcessorEJs("test-api-key")
    
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

def test_empresa_duplicada_sem_nome():
    """Testa detecção de empresas sem nome"""
    processor = PDFProcessorEJs("test-api-key")
    
    empresas_existentes = [{"Nome": "Empresa A"}]
    empresa_sem_nome = {"Cursos": "Engenharia"}
    
    assert processor.empresa_duplicada(empresa_sem_nome, empresas_existentes) is False

def test_salvar_json():
    """Testa salvamento de JSON"""
    processor = PDFProcessorEJs("test-api-key")
    
    dados_teste = [
        {"Nome": "Empresa A", "Cursos": "Engenharia"},
        {"Nome": "Empresa B", "Cursos": "Computação"}
    ]
    
    # Usar TemporaryDirectory em vez de NamedTemporaryFile para evitar problemas no Windows
    with tempfile.TemporaryDirectory() as temp_dir:
        caminho_arquivo = os.path.join(temp_dir, "test.json")
        processor.salvar_json(dados_teste, caminho_arquivo)
        
        # Verifica se o arquivo foi criado
        assert os.path.exists(caminho_arquivo)
        
        # Verifica se o conteúdo está correto
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados_salvos = json.load(f)
        
        assert len(dados_salvos) == 2
        assert dados_salvos[0]['Nome'] == "Empresa A"
        assert dados_salvos[1]['Cursos'] == "Computação"

def test_salvar_json_erro():
    """Testa salvamento de JSON com erro"""
    processor = PDFProcessorEJs("test-api-key")
    
    dados_teste = [{"teste": "dados"}]
    
    # Mock do print para capturar mensagem de erro
    mock_print = Mock()
    
    with patch('builtins.print', mock_print), \
         patch('builtins.open', side_effect=Exception("Erro de IO")):
        
        processor.salvar_json(dados_teste, "/caminho/inexistente/arquivo.json")
        
        # Verifica se a mensagem de erro foi impressa
        mock_print.assert_any_call("✗ Erro ao salvar JSON: Erro de IO")

@patch('pdf_processor_ejs.requests.get')
def test_baixar_pdf_direto_sucesso(mock_requests):
    """Testa download bem-sucedido de PDF"""
    processor = PDFProcessorEJs("test-api-key")
    
    # Mock da resposta
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.iter_content.return_value = [b"pdf content"]
    mock_requests.return_value = mock_response
    
    with tempfile.TemporaryDirectory() as temp_dir:
        caminho_saida = os.path.join(temp_dir, "test.pdf")
        resultado = processor.baixar_pdf_direto("http://example.com/test.pdf", caminho_saida)
        
        assert resultado == caminho_saida
        assert os.path.exists(caminho_saida)
        
        # Verifica se o requests.get foi chamado corretamente
        mock_requests.assert_called_once_with(
            "http://example.com/test.pdf",
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout=30,
            stream=True
        )

@patch('pdf_processor_ejs.requests.get')
def test_baixar_pdf_direto_erro(mock_requests):
    """Testa download de PDF com erro"""
    processor = PDFProcessorEJs("test-api-key")
    
    mock_requests.side_effect = Exception("Erro de conexão")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        caminho_saida = os.path.join(temp_dir, "test.pdf")
        
        with pytest.raises(Exception, match="Erro de conexão"):
            processor.baixar_pdf_direto("http://example.com/test.pdf", caminho_saida)

@patch('pdf_processor_ejs.pdfplumber.open')
def test_extrair_texto_por_pagina(mock_pdfplumber):
    """Testa extração de texto por página"""
    processor = PDFProcessorEJs("test-api-key")
    
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
def test_extrair_texto_por_pagina_vazia(mock_pdfplumber):
    """Testa extração de texto de página vazia"""
    processor = PDFProcessorEJs("test-api-key")
    
    mock_page = Mock()
    mock_page.extract_text.return_value = ""  # Página vazia
    
    mock_pdf = Mock()
    mock_pdf.pages = [mock_page]
    mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
    
    with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
        resultado = processor.extrair_texto_por_pagina(temp_file.name)
        
        assert len(resultado) == 0

@patch('pdf_processor_ejs.pdfplumber.open')
def test_extrair_texto_por_pagina_com_pagina_inicial(mock_pdfplumber):
    """Testa extração de texto com página inicial específica"""
    processor = PDFProcessorEJs("test-api-key")
    
    # Mock de 5 páginas
    mock_pages = []
    for i in range(5):
        mock_page = Mock()
        mock_page.extract_text.return_value = f"Texto página {i+1}"
        mock_pages.append(mock_page)
    
    mock_pdf = Mock()
    mock_pdf.pages = mock_pages
    mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
    
    with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
        # Extrai a partir da página 3
        resultado = processor.extrair_texto_por_pagina(temp_file.name, pagina_inicial=3)
        
        # Deve retornar apenas páginas 3, 4, 5
        assert len(resultado) == 3
        assert resultado[0]['texto'] == "Texto página 3"
        assert resultado[1]['texto'] == "Texto página 4"
        assert resultado[2]['texto'] == "Texto página 5"

def test_extrair_imagens_pdf(mocker):
    """Testa extração de imagens do PDF"""
    processor = PDFProcessorEJs("test-api-key")
    
    # Mock do fitz.open usando MagicMock para métodos mágicos
    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 1  # 1 página
    mock_page = MagicMock()
    mock_page.get_images.return_value = [(1,)]  # Uma imagem na página
    
    mock_doc.__getitem__.return_value = mock_page
    mock_doc.extract_image.return_value = {
        "image": b"fake image data",
        "ext": "png"
    }
    
    mock_fitz = mocker.patch('pdf_processor_ejs.fitz.open')
    mock_fitz.return_value = mock_doc
    
    # Mock do config_ej - patchando o import dentro do pdf_processor_ejs
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock das variáveis do config_ej que são importadas
        with patch('pdf_processor_ejs.IMAGES_OUTPUT_DIR', temp_dir, create=True), \
             patch('pdf_processor_ejs.os.makedirs'), \
             patch('builtins.open', mocker.mock_open()):
            
            with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
                resultado = processor.extrair_imagens_pdf(temp_file.name, temp_dir)
                
                # Verifica se a função retornou uma lista
                assert isinstance(resultado, list)

def test_extrair_imagens_pdf_com_empresas_ids(mocker):
    """Testa extração de imagens com mapeamento de empresas"""
    processor = PDFProcessorEJs("test-api-key")
    
    # Mock do fitz.open usando MagicMock
    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 3  # 3 páginas
    mock_page = MagicMock()
    mock_page.get_images.return_value = [(1,)]  # Uma imagem por página
    
    mock_doc.__getitem__.return_value = mock_page
    mock_doc.extract_image.return_value = {
        "image": b"fake image data",
        "ext": "png"
    }
    
    mock_fitz = mocker.patch('pdf_processor_ejs.fitz.open')
    mock_fitz.return_value = mock_doc
    
    empresas_com_id = [
        {"id": "100001", "Nome": "Empresa A"},
        {"id": "100002", "Nome": "Empresa B"}
    ]
    
    # Mock do config_ej - patchando o import dentro do pdf_processor_ejs
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock das variáveis do config_ej que são importadas
        with patch('pdf_processor_ejs.IMAGES_OUTPUT_DIR', temp_dir, create=True), \
             patch('pdf_processor_ejs.PAGINA_INICIAL_EJS', 1, create=True), \
             patch('pdf_processor_ejs.os.makedirs'), \
             patch('builtins.open', mocker.mock_open()):
            
            with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
                resultado = processor.extrair_imagens_pdf(
                    temp_file.name, 
                    temp_dir, 
                    empresas_com_id
                )
                
                assert isinstance(resultado, list)

@patch('pdf_processor_ejs.pdfplumber.open')
@patch.object(PDFProcessorEJs, 'extrair_informacoes_gemini')
def test_processar_pdf_paginado(mock_extrair_gemini, mock_pdfplumber):
    """Testa processamento paginado do PDF"""
    processor = PDFProcessorEJs("test-api-key")
    
    # Mock dos dados de texto
    mock_pages = []
    for i in range(4):
        mock_page = Mock()
        mock_page.extract_text.return_value = f"Texto página {i+1}"
        mock_pages.append(mock_page)
    
    mock_pdf = Mock()
    mock_pdf.pages = mock_pages
    mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
    
    # Mock da resposta do Gemini
    mock_extrair_gemini.return_value = [
        {"Nome": "Empresa Teste", "Cursos": "Engenharia"}
    ]
    
    # Mock das dependências - patchando as importações do config_ej
    with patch('pdf_processor_ejs.OUTPUT_DIR', tempfile.gettempdir(), create=True), \
         patch('pdf_processor_ejs.EXTRAIR_IMAGENS', False, create=True), \
         patch('pdf_processor_ejs.time.sleep'), \
         patch.object(processor, 'extrair_imagens_pdf', return_value=[]), \
         patch.object(processor, 'salvar_json'):
        
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, "test.pdf")
            json_path = os.path.join(temp_dir, "output.json")
            
            # Cria arquivo PDF vazio para o teste
            with open(pdf_path, 'w') as f:
                f.write("fake pdf content")
            
            resultado = processor.processar_pdf_paginado(pdf_path, json_path)
            
            assert len(resultado) > 0
            # Verifica se os IDs foram gerados
            assert 'id' in resultado[0]
            assert resultado[0]['id'].startswith('1')

def test_extrair_informacoes_gemini_sucesso(mocker):
    """Testa extração bem-sucedida com Gemini"""
    processor = PDFProcessorEJs("test-api-key")
    
    # Mock do modelo Gemini
    mock_response = Mock()
    mock_response.text = '[{"Nome": "Empresa Teste", "Cursos": "Engenharia"}]'
    
    mock_generate = Mock()
    mock_generate.generate_content.return_value = mock_response
    
    # Mock do modelo usando mocker.patch para evitar problemas de importação
    mock_model = mocker.patch.object(processor, 'model')
    mock_model.generate_content.return_value = mock_response
    
    resultado = processor.extrair_informacoes_gemini("Texto de teste")
    
    assert len(resultado) == 1
    assert resultado[0]['Nome'] == "Empresa Teste"

def test_extrair_informacoes_gemini_json_invalido(mocker):
    """Testa extração com JSON inválido do Gemini"""
    processor = PDFProcessorEJs("test-api-key")
    
    # Mock da resposta com JSON inválido
    mock_response = Mock()
    mock_response.text = 'JSON inválido { Nome: "Empresa" }'
    
    mock_model = mocker.patch.object(processor, 'model')
    mock_model.generate_content.return_value = mock_response
    
    resultado = processor.extrair_informacoes_gemini("Texto de teste")
    
    # Deve retornar lista vazia quando não consegue processar JSON
    assert resultado == []

def test_extrair_informacoes_gemini_dict_instead_of_list(mocker):
    """Testa extração quando Gemini retorna dict em vez de lista"""
    processor = PDFProcessorEJs("test-api-key")
    
    # Mock da resposta com dict em vez de lista
    mock_response = Mock()
    mock_response.text = '{"Nome": "Empresa Teste", "Cursos": "Engenharia"}'
    
    mock_model = mocker.patch.object(processor, 'model')
    mock_model.generate_content.return_value = mock_response
    
    resultado = processor.extrair_informacoes_gemini("Texto de teste")
    
    # Deve converter dict para lista
    assert len(resultado) == 1
    assert resultado[0]['Nome'] == "Empresa Teste"

def test_processar_pdf_paginado_sem_texto():
    """Testa processamento quando não há texto extraído"""
    processor = PDFProcessorEJs("test-api-key")
    
    with patch.object(processor, 'extrair_texto_por_pagina', return_value=[]):
        resultado = processor.processar_pdf_paginado("caminho/fake.pdf", "saida.json")
        
        assert resultado == []