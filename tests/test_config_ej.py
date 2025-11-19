"""
Testes unitários para config_ej.py
"""
import os
import pytest
import sys
from unittest.mock import patch, MagicMock

# Adiciona o diretório scripts ao path para importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_config_ej_constantes_definidas():
    """Testa se todas as constantes estão definidas"""
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'}):
        # Import dentro do teste para evitar efeitos colaterais
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

def test_config_ej_api_key_nao_configurada(capsys):
    """Testa o aviso quando API_KEY não está configurada"""
    with patch.dict(os.environ, {}, clear=True):
        
        if 'scripts.config_ej' in sys.modules:
            del sys.modules['scripts.config_ej']
        
        import scripts.config_ej as config
        
        
        captured = capsys.readouterr()
        assert "AVISO: GEMINI_API_KEY não configurada" in captured.out
        assert "configure a variável de ambiente" in captured.out

def test_config_ej_api_key_configurada(mocker):
    """Testa quando API_KEY está configurada corretamente"""
    mock_configure = mocker.patch('scripts.config_ej.genai.configure')
    
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'chave-valida-teste'}):
        
        if 'scripts.config_ej' in sys.modules:
            del sys.modules['scripts.config_ej']
        
        import scripts.config_ej as config
        
        
        mock_configure.assert_called_once_with(api_key='chave-valida-teste')

def test_config_ej_valores_padrao():
    """Testa os valores padrão das configurações"""
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'}):
        if 'scripts.config_ej' in sys.modules:
            del sys.modules['scripts.config_ej']
        
        import scripts.config_ej as config
        
        assert config.PDF_URL_EJS == "https://unb.br/images/Noticias/2023/Documentos/PORTFLIO_EJS.pdf"
        assert config.OUTPUT_JSON == "empresas_juniores_consolidadas.json"
        assert config.PROCESSAR_POR_PAGINA is True
        assert config.MAX_PAGINAS_POR_REQUISICAO == 10
        assert config.PAGINA_INICIAL_EJS == 6
        assert config.EXTRAIR_IMAGENS is True