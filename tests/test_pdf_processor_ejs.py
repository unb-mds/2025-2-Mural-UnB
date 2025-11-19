"""
Testes unitários para pdf_processor_ejs.py
"""
import os
import sys
import pytest
import json
import numpy as np
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

@pytest.fixture
def mock_gemini_api():
    """Fixture para mock da API Gemini"""
    with patch('scripts.pdf_processor_ejs.genai.configure') as mock_configure, \
         patch('scripts.pdf_processor_ejs.genai.GenerativeModel') as mock_model:
        
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        mock_configure.return_value = None
        
        yield mock_model_instance

def test_pdf_processor_init(mock_gemini_api):
    """Testa inicialização do PDFProcessorEJs"""
    from scripts.pdf_processor_ejs import PDFProcessorEJs
    
    processor = PDFProcessorEJs("fake-api-key")
    
    assert processor.gemini_api_key == "fake-api-key"
    assert processor.model is not None

def test_limpar_texto():
    """Testa a limpeza de texto"""
    from scripts.pdf_processor_ejs import PDFProcessorEJs
    
    processor = PDFProcessorEJs("fake-key")
    texto_sujo = "Texto\u202fcom\u00a0caracteres\u2013especiais\u2014problema\u2019ticoss"
    texto_limpo = processor.limpar_texto(texto_sujo)
    
    assert "\u202f" not in texto_limpo
    assert "\u00a0" not in texto_limpo
    assert "\u2013" not in texto_limpo

def test_juntar_palavras_hifenizadas():
    """Testa a correção de palavras hifenizadas"""
    from scripts.pdf_processor_ejs import PDFProcessorEJs
    
    processor = PDFProcessorEJs("fake-key")
    texto_com_hifen = "Esta é uma pala- vra hifenizada no final da linha."
    texto_corrigido = processor.juntar_palavras_hifenizadas(texto_com_hifen)
    
    assert "pala- vra" not in texto_corrigido
    assert "palavra" in texto_corrigido

def test_criar_prompt_gemini():
    """Testa a criação do prompt para Gemini"""
    from scripts.pdf_processor_ejs import PDFProcessorEJs
    
    processor = PDFProcessorEJs("fake-key")
    texto_teste = "Texto de exemplo para extração"
    prompt = processor.criar_prompt_gemini(texto_teste, "Página 1")
    
    assert "ANALISE O TEXTO E EXTRAIA INFORMAÇÕES" in prompt
    assert texto_teste in prompt
    assert "FORMATO DE SAÍDA EXATO" in prompt

def test_limpar_e_corrigir_json():
    """Testa a limpeza e correção de JSON"""
    from scripts.pdf_processor_ejs import PDFProcessorEJs
    
    processor = PDFProcessorEJs("fake-key")
    
    # Teste com markdown
    json_com_markdown = "```json\n[{\"Nome\": \"Teste\"}]\n```"
    resultado = processor.limpar_e_corrigir_json(json_com_markdown)
    assert "```" not in resultado
    
    # Teste com texto antes do JSON
    json_com_texto = "Aqui está o JSON: [{\"Nome\": \"Teste\"}]"
    resultado = processor.limpar_e_corrigir_json(json_com_texto)
    assert resultado.startswith('[')
    
    # Teste com vírgula trailing
    json_com_virgula = "[{\"Nome\": \"Teste\"},]"
    resultado = processor.limpar_e_corrigir_json(json_com_virgula)
    assert resultado == "[{\"Nome\": \"Teste\"}]"

def test_extrair_informacoes_gemini_sucesso(mock_gemini_api):
    """Testa extração bem-sucedida com Gemini"""
    from scripts.pdf_processor_ejs import PDFProcessorEJs
    
    processor = PDFProcessorEJs("fake-key")
    
    # Mock da resposta do Gemini
    resposta_json = '[{"Nome": "Empresa Teste", "Cursos": "Engenharia", "Sobre": "Descrição"}]'
    mock_resposta = MagicMock()
    mock_resposta.text = resposta_json
    mock_gemini_api.generate_content.return_value = mock_resposta
    
    texto_teste = "Texto sobre empresa júnior"
    resultado = processor.extrair_informacoes_gemini(texto_teste)
    
    assert len(resultado) == 1
    assert resultado[0]["Nome"] == "Empresa Teste"
    mock_gemini_api.generate_content.assert_called_once()

def test_extrair_informacoes_gemini_json_invalido(mock_gemini_api):
    """Testa comportamento com JSON inválido do Gemini"""
    from scripts.pdf_processor_ejs import PDFProcessorEJs
    
    processor = PDFProcessorEJs("fake-key")
    
    # Mock com JSON inválido
    mock_resposta = MagicMock()
    mock_resposta.text = "JSON inválido {"
    mock_gemini_api.generate_content.return_value = mock_resposta
    
    resultado = processor.extrair_informacoes_gemini("texto")
    
    assert resultado == []  # Deve retornar lista vazia em caso de erro

def test_empresa_duplicada():
    """Testa detecção de empresas duplicadas"""
    from scripts.pdf_processor_ejs import PDFProcessorEJs
    
    processor = PDFProcessorEJs("fake-key")
    
    empresas_existentes = [
        {"Nome": "Empresa A", "Cursos": "Engenharia"},
        {"Nome": "Empresa B", "Cursos": "Computação"}
    ]
    
    nova_empresa = {"Nome": "Empresa A", "Cursos": "Engenharia Civil"}
    
    # Deve detectar como duplicada
    assert processor.empresa_duplicada(nova_empresa, empresas_existentes) is True
    
    # Empresa diferente não deve ser detectada como duplicada
    nova_empresa_diferente = {"Nome": "Empresa C", "Cursos": "Medicina"}
    assert processor.empresa_duplicada(nova_empresa_diferente, empresas_existentes) is False

def test_salvar_json(mocker):
    """Testa salvamento de JSON"""
    from scripts.pdf_processor_ejs import PDFProcessorEJs
    
    processor = PDFProcessorEJs("fake-key")
    mock_open_file = mocker.patch('builtins.open', mock_open())
    mock_json_dump = mocker.patch('scripts.pdf_processor_ejs.json.dump')
    
    dados_teste = [{"Nome": "Empresa Teste"}]
    processor.salvar_json(dados_teste, "teste.json")
    
    mock_open_file.assert_called_once_with("teste.json", 'w', encoding='utf-8')
    mock_json_dump.assert_called_once()