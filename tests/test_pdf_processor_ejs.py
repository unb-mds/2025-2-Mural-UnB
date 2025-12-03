import pytest
import os
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock, ANY
import sys

# Adiciona o caminho para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Importa o módulo inteiro para poder manipular globais
import scripts.pdf_processor_ejs
from scripts.pdf_processor_ejs import PDFProcessorEJs

# --- Fixture para mockar config_ej globalmente ---
@pytest.fixture
def mock_config_ej():
    # Cria um mock para o módulo config_ej
    mock_module = MagicMock()
    # Define valores padrão
    mock_module.IMAGES_OUTPUT_DIR = "/tmp/images"
    mock_module.EXTRAIR_IMAGENS = True
    mock_module.PAGINA_INICIAL_EJS = 1
    
    # Injeta o mock no sys.modules
    with patch.dict(sys.modules, {'config_ej': mock_module}):
        yield mock_module

# --- Testes de Inicialização e Helpers ---

def test_pdf_processor_ejs_init(mocker):
    mock_configure = mocker.patch('scripts.pdf_processor_ejs.genai.configure')
    processor = PDFProcessorEJs("test-api-key")
    assert processor.gemini_api_key == "test-api-key"
    mock_configure.assert_called_once_with(api_key="test-api-key")

def test_limpar_texto():
    processor = PDFProcessorEJs("k")
    texto = "Texto\u202fcom\xa0sujeira\u2013e\u2014traços"
    limpo = processor.limpar_texto(texto)
    assert limpo == "Texto com sujeira-e-traços"
    assert processor.limpar_texto(None) is None

def test_juntar_palavras_hifenizadas():
    processor = PDFProcessorEJs("k")
    texto = "pala-\n vra"
    assert processor.juntar_palavras_hifenizadas(texto) == "palavra"
    assert processor.juntar_palavras_hifenizadas(None) is None

def test_criar_prompt_gemini():
    processor = PDFProcessorEJs("k")
    prompt = processor.criar_prompt_gemini("texto")
    assert "ANALISE O TEXTO" in prompt
    assert "texto" in prompt

# --- Testes de Manipulação de JSON ---

def test_limpar_e_corrigir_json():
    processor = PDFProcessorEJs("k")
    assert processor.limpar_e_corrigir_json("```json\n[1]\n```") == "[1]"
    assert processor.limpar_e_corrigir_json("lixo [1] lixo") == "[1]"
    assert processor.limpar_e_corrigir_json("{'a':1}") == "[{'a':1}]"

def test_corrigir_json_agressivo():
    processor = PDFProcessorEJs("k")
    ruim = "{'nome': 'valor'}" 
    corrigido = processor.corrigir_json(ruim)
    assert '"nome": "valor"' in corrigido
    assert corrigido.startswith('[')

# --- Testes de Download e Texto ---

@patch('scripts.pdf_processor_ejs.requests.get')
def test_baixar_pdf_direto(mock_get):
    processor = PDFProcessorEJs("k")
    mock_response = Mock()
    mock_response.iter_content.return_value = [b"pdf"]
    mock_get.return_value = mock_response
    
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "t.pdf")
        assert processor.baixar_pdf_direto("http://url", path) == path
        assert os.path.exists(path)

@patch('scripts.pdf_processor_ejs.requests.get')
def test_baixar_pdf_erro(mock_get):
    processor = PDFProcessorEJs("k")
    mock_get.side_effect = Exception("Erro")
    with pytest.raises(Exception):
        processor.baixar_pdf_direto("http://url", "path")

@patch('scripts.pdf_processor_ejs.pdfplumber.open')
def test_extrair_texto_por_pagina(mock_pdf_open):
    processor = PDFProcessorEJs("k")
    
    page_mock = Mock()
    page_mock.extract_text.return_value = "Texto Pagina"
    
    pdf_mock = MagicMock()
    pdf_mock.pages = [page_mock]
    mock_pdf_open.return_value.__enter__.return_value = pdf_mock
    
    res = processor.extrair_texto_por_pagina("f.pdf")
    assert len(res) == 1
    assert res[0]['texto'] == "Texto Pagina"

@patch('scripts.pdf_processor_ejs.pdfplumber.open')
def test_extrair_texto_exception(mock_pdf_open):
    processor = PDFProcessorEJs("k")
    mock_pdf_open.side_effect = Exception("Erro PDF")
    res = processor.extrair_texto_por_pagina("f.pdf")
    assert res == []

# --- Testes Complexos: Imagens ---

def test_extrair_imagens_pdf_fluxo_completo(mocker, mock_config_ej):
    processor = PDFProcessorEJs("k")
    
    # CORREÇÃO: Forçar a variável global no módulo importado para 1
    # Isso garante que a lógica PAGINA_INICIAL_EJS + i funcione com index 0
    scripts.pdf_processor_ejs.PAGINA_INICIAL_EJS = 1
    
    # Mock do Fitz
    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 1
    
    page1 = MagicMock()
    page1.get_images.return_value = [(1,)] # 1 imagem na pag 1
    mock_doc.__getitem__.return_value = page1
    mock_doc.extract_image.return_value = {"image": b"bytes", "ext": "png"}
    
    mocker.patch('scripts.pdf_processor_ejs.fitz.open', return_value=mock_doc)
    
    # Mock de IO
    mocker.patch('os.makedirs')
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    
    # Configura valores no mock do config_ej (usado dentro da função)
    mock_config_ej.IMAGES_OUTPUT_DIR = '/tmp/imgs'
    
    empresas = [{'id': 'ej1', 'Nome': 'EJ Teste'}]
    
    # Executa a função
    res = processor.extrair_imagens_pdf("doc.pdf", "/tmp", empresas)
    
    # Deve ter extraído a imagem da página 1 (PAGINA_INICIAL 1 + offset 0)
    assert len(res) >= 1
    assert res[0]['id_ej_associado'] == 'ej1'

def test_extrair_imagens_pdf_exception(mocker, mock_config_ej):
    processor = PDFProcessorEJs("k")
    mocker.patch('scripts.pdf_processor_ejs.fitz.open', side_effect=Exception("Erro Fitz"))
    
    # Configura valor no mock do config_ej
    mock_config_ej.IMAGES_OUTPUT_DIR = '/tmp'
    
    res = processor.extrair_imagens_pdf("doc.pdf", "/tmp")
    assert res == []

# --- Testes Complexos: Gemini e Processamento ---

def test_extrair_informacoes_gemini_sucesso(mocker):
    processor = PDFProcessorEJs("k")
    mock_resp = Mock()
    mock_resp.text = '[{"Nome": "EJ"}]'
    processor.model.generate_content = Mock(return_value=mock_resp)
    
    res = processor.extrair_informacoes_gemini("texto")
    assert len(res) == 1
    assert res[0]['Nome'] == "EJ"

def test_extrair_informacoes_gemini_retry_sucesso(mocker):
    processor = PDFProcessorEJs("k")
    mock_resp = Mock()
    mock_resp.text = "{'Nome': 'EJ'}"
    processor.model.generate_content = Mock(return_value=mock_resp)
    
    res = processor.extrair_informacoes_gemini("texto")
    assert len(res) == 1
    assert res[0]['Nome'] == "EJ"

def test_extrair_informacoes_gemini_retry_falha(mocker):
    processor = PDFProcessorEJs("k")
    mock_resp = Mock()
    mock_resp.text = "Lixo"
    processor.model.generate_content = Mock(return_value=mock_resp)
    res = processor.extrair_informacoes_gemini("texto")
    assert res == []

def test_extrair_informacoes_gemini_exception_geral(mocker):
    processor = PDFProcessorEJs("k")
    processor.model.generate_content = Mock(side_effect=Exception("API Error"))
    res = processor.extrair_informacoes_gemini("texto")
    assert res == []

def test_processar_pdf_paginado_completo(mocker, mock_config_ej):
    processor = PDFProcessorEJs("k")
    
    # 1. Mock texto
    pages_data = [
        {'numero_pagina': 1, 'texto': 'p1'},
        {'numero_pagina': 2, 'texto': 'p2'},
        {'numero_pagina': 3, 'texto': 'p3'}
    ]
    mocker.patch.object(processor, 'extrair_texto_por_pagina', return_value=pages_data)
    
    # 2. Mock Gemini
    mocker.patch.object(processor, 'extrair_informacoes_gemini', side_effect=[
        [{'Nome': 'EJ 1'}], [{'Nome': 'EJ 2'}]
    ])
    
    # 3. Mock Helpers
    mocker.patch.object(processor, 'salvar_json')
    mocker.patch.object(processor, 'extrair_imagens_pdf', return_value=[])
    mocker.patch('scripts.pdf_processor_ejs.time.sleep')
    
    # CORREÇÃO: Setar variável diretamente no mock do config_ej
    # Isso funciona porque a função faz 'from config_ej import EXTRAIR_IMAGENS'
    mock_config_ej.EXTRAIR_IMAGENS = True
    mock_config_ej.OUTPUT_DIR = '/tmp'
    
    res = processor.processar_pdf_paginado("doc.pdf", "out.json", max_paginas_por_requisicao=2)
    
    assert len(res) == 2
    assert res[0]['id'] == '100001'
    assert res[1]['id'] == '100002'

def test_processar_pdf_paginado_sem_texto(mocker):
    processor = PDFProcessorEJs("k")
    mocker.patch.object(processor, 'extrair_texto_por_pagina', return_value=[])
    res = processor.processar_pdf_paginado("doc.pdf", "out.json")
    assert res == []