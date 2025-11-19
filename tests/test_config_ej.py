"""
Testes unitários para config_ej.py - Versão robusta
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_config_ej_constantes_definidas():
    """Testa se todas as constantes estão definidas"""
    
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'}), \
         patch('scripts.config_ej.genai.configure') as mock_configure:
        
        
        if 'scripts.config_ej' in sys.modules:
            del sys.modules['scripts.config_ej']
        import scripts.config_ej as config
        
        
        assert hasattr(config, 'GEMINI_API_KEY')
        assert hasattr(config, 'PDF_URL_EJS')
        assert hasattr(config, 'OUTPUT_DIR')
        assert hasattr(config, 'OUTPUT_JSON')
        assert hasattr(config, 'IMAGES_DIR')
        assert hasattr(config, 'PROCESSAR_POR_PAGINA')
        assert hasattr(config, 'MAX_PAGINAS_POR_REQUISICAO')
        assert hasattr(config, 'PAGINA_INICIAL_EJS')
        assert hasattr(config, 'EXTRAIR_IMAGENS')

def test_config_ej_comportamento_sem_api_key():
    """Testa o COMPORTAMENTO quando API_KEY não está configurada"""
    
    with patch.dict(os.environ, {}, clear=True), \
         patch('builtins.print') as mock_print:
        
        
        with patch('scripts.config_ej.GEMINI_API_KEY', 'sua_chave_aqui'), \
             patch('scripts.config_ej.genai.configure') as mock_configure:
            
            
            if 'scripts.config_ej' in sys.modules:
                del sys.modules['scripts.config_ej']
            import scripts.config_ej as config
            

            assert mock_print.called, "Deveria mostrar aviso quando API key não está configurada"
            assert not mock_configure.called, "Não deveria configurar Gemini sem API key válida"

def test_config_ej_comportamento_com_api_key_valida():
    """Testa o COMPORTAMENTO quando API_KEY está configurada corretamente"""
    
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'chave-valida-123'}), \
         patch('scripts.config_ej.genai.configure') as mock_configure:
        
        
        with patch('scripts.config_ej.GEMINI_API_KEY', 'chave-valida-123'):
            
            
            if 'scripts.config_ej' in sys.modules:
                del sys.modules['scripts.config_ej']
            import scripts.config_ej as config
            
            
            mock_configure.assert_called_once_with(api_key='chave-valida-123')

def test_config_ej_comportamento_com_api_key_invalida():
    """Testa o COMPORTAMENTO quando API_KEY tem valor inválido (igual ao padrão)"""
    
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'sua_chave_aqui'}), \
         patch('builtins.print') as mock_print, \
         patch('scripts.config_ej.genai.configure') as mock_configure:
        
        
        if 'scripts.config_ej' in sys.modules:
            del sys.modules['scripts.config_ej']
        import scripts.config_ej as config
        
        
        assert mock_print.called, "Deveria avisar quando API key tem valor padrão"
        assert not mock_configure.called, "Não deveria configurar Gemini com valor padrão"

def test_config_ej_valores_estrutura():
    """Testa apenas a estrutura/valores fixos das configurações (isolado do ambiente)"""
    
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'mock-key'}), \
         patch('scripts.config_ej.genai.configure'):
        
        if 'scripts.config_ej' in sys.modules:
            del sys.modules['scripts.config_ej']
        import scripts.config_ej as config
        
        
        assert config.PDF_URL_EJS == "https://unb.br/images/Noticias/2023/Documentos/PORTFLIO_EJS.pdf"
        assert config.OUTPUT_JSON == "empresas_juniores_consolidadas.json"
        assert config.PROCESSAR_POR_PAGINA is True
        assert config.MAX_PAGINAS_POR_REQUISICAO == 10
        assert config.PAGINA_INICIAL_EJS == 6
        assert config.EXTRAIR_IMAGENS is True