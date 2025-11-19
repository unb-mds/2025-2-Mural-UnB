"""
Testes unitários para config_ej.py - Versão robusta
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Adiciona o diretório scripts ao path para importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_config_ej_constantes_definidas():
    """Testa se todas as constantes estão definidas"""
    # Mock completo para isolar o teste do ambiente real
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'}), \
         patch('scripts.config_ej.genai.configure') as mock_configure:
        
        # Recarrega o módulo com ambiente controlado
        if 'scripts.config_ej' in sys.modules:
            del sys.modules['scripts.config_ej']
        import scripts.config_ej as config
        
        # Verifica apenas se as constantes existem
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
    # Cenário 1: Variável de ambiente vazia E valor padrão no código
    with patch.dict(os.environ, {}, clear=True), \
         patch('builtins.print') as mock_print:
        
        # Precisamos mockar o valor dentro do próprio módulo config_ej
        with patch('scripts.config_ej.GEMINI_API_KEY', 'sua_chave_aqui'), \
             patch('scripts.config_ej.genai.configure') as mock_configure:
            
            # Recarrega o módulo
            if 'scripts.config_ej' in sys.modules:
                del sys.modules['scripts.config_ej']
            import scripts.config_ej as config
            
            # COMPORTAMENTO ESPERADO: print de aviso deve ser chamado
            # E genai.configure NÃO deve ser chamado
            assert mock_print.called, "Deveria mostrar aviso quando API key não está configurada"
            assert not mock_configure.called, "Não deveria configurar Gemini sem API key válida"

def test_config_ej_comportamento_com_api_key_valida():
    """Testa o COMPORTAMENTO quando API_KEY está configurada corretamente"""
    # Cenário 2: Variável de ambiente com chave válida
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'chave-valida-123'}), \
         patch('scripts.config_ej.genai.configure') as mock_configure:
        
        # Mock do valor no módulo para simular que pegou da env var
        with patch('scripts.config_ej.GEMINI_API_KEY', 'chave-valida-123'):
            
            # Recarrega o módulo
            if 'scripts.config_ej' in sys.modules:
                del sys.modules['scripts.config_ej']
            import scripts.config_ej as config
            
            # COMPORTAMENTO ESPERADO: genai.configure deve ser chamado com a chave
            mock_configure.assert_called_once_with(api_key='chave-valida-123')

def test_config_ej_comportamento_com_api_key_invalida():
    """Testa o COMPORTAMENTO quando API_KEY tem valor inválido (igual ao padrão)"""
    # Cenário 3: Variável de ambiente com valor igual ao padrão
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'sua_chave_aqui'}), \
         patch('builtins.print') as mock_print, \
         patch('scripts.config_ej.genai.configure') as mock_configure:
        
        # Recarrega o módulo
        if 'scripts.config_ej' in sys.modules:
            del sys.modules['scripts.config_ej']
        import scripts.config_ej as config
        
        # COMPORTAMENTO ESPERADO: print de aviso E genai.configure NÃO chamado
        assert mock_print.called, "Deveria avisar quando API key tem valor padrão"
        assert not mock_configure.called, "Não deveria configurar Gemini com valor padrão"

def test_config_ej_valores_estrutura():
    """Testa apenas a estrutura/valores fixos das configurações (isolado do ambiente)"""
    # Mock completo para testar valores fixos independentemente do ambiente
    with patch.dict(os.environ, {'GEMINI_API_KEY': 'mock-key'}), \
         patch('scripts.config_ej.genai.configure'):
        
        if 'scripts.config_ej' in sys.modules:
            del sys.modules['scripts.config_ej']
        import scripts.config_ej as config
        
        # Testa apenas valores que NÃO dependem do ambiente/API key
        assert config.PDF_URL_EJS == "https://unb.br/images/Noticias/2023/Documentos/PORTFLIO_EJS.pdf"
        assert config.OUTPUT_JSON == "empresas_juniores_consolidadas.json"
        assert config.PROCESSAR_POR_PAGINA is True
        assert config.MAX_PAGINAS_POR_REQUISICAO == 10
        assert config.PAGINA_INICIAL_EJS == 6
        assert config.EXTRAIR_IMAGENS is True