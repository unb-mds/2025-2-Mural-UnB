"""
Testes unitários para config_ej.py
"""
import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Adiciona o caminho para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

class TestConfigEJ:
    """Testes para o arquivo de configuração config_ej.py"""

    def test_configuracoes_existem(self):
        """Verifica se todas as configurações necessárias existem"""
        from scripts.config_ej import (
            GEMINI_API_KEY, PDF_URL_EJS, OUTPUT_DIR, IMAGES_OUTPUT_DIR,
            OUTPUT_JSON, PROCESSAR_POR_PAGINA, MAX_PAGINAS_POR_REQUISICAO,
            PAGINA_INICIAL_EJS, EXTRAIR_IMAGENS
        )
        
        # Verifica se todas as variáveis estão definidas
        assert GEMINI_API_KEY is not None
        assert PDF_URL_EJS is not None
        assert OUTPUT_DIR is not None
        assert IMAGES_OUTPUT_DIR is not None
        assert OUTPUT_JSON is not None
        assert PROCESSAR_POR_PAGINA is not None
        assert MAX_PAGINAS_POR_REQUISICAO is not None
        assert PAGINA_INICIAL_EJS is not None
        assert EXTRAIR_IMAGENS is not None

    def test_caminhos_diretorios(self):
        """Verifica se os caminhos dos diretórios são válidos"""
        from scripts.config_ej import OUTPUT_DIR, IMAGES_OUTPUT_DIR

        # Verifica se os caminhos são strings
        assert isinstance(OUTPUT_DIR, str)
        assert isinstance(IMAGES_OUTPUT_DIR, str)

        # Verifica se os caminhos contêm os diretórios esperados (independente do SO)
        assert "data" in OUTPUT_DIR
        assert "EJs" in OUTPUT_DIR
        assert "images" in IMAGES_OUTPUT_DIR
        assert "EJs" in IMAGES_OUTPUT_DIR

        # Verifica se os caminhos são absolutos (ou pelo menos válidos)
        assert os.path.isabs(OUTPUT_DIR) or ".." in OUTPUT_DIR
        assert os.path.isabs(IMAGES_OUTPUT_DIR) or ".." in IMAGES_OUTPUT_DIR

    def test_valores_configuracao(self):
        """Verifica se os valores de configuração são válidos"""
        from scripts.config_ej import (
            PDF_URL_EJS, OUTPUT_JSON, PROCESSAR_POR_PAGINA,
            MAX_PAGINAS_POR_REQUISICAO, PAGINA_INICIAL_EJS, EXTRAIR_IMAGENS
        )
        
        # Verifica URL do PDF
        assert PDF_URL_EJS.startswith('http')
        assert "unb.br" in PDF_URL_EJS
        
        # Verifica nome do arquivo JSON
        assert OUTPUT_JSON.endswith('.json')
        assert "empresas_juniores" in OUTPUT_JSON
        
        # Verifica tipos e valores
        assert isinstance(PROCESSAR_POR_PAGINA, bool)
        assert isinstance(MAX_PAGINAS_POR_REQUISICAO, int)
        assert MAX_PAGINAS_POR_REQUISICAO > 0
        assert isinstance(PAGINA_INICIAL_EJS, int)
        assert PAGINA_INICIAL_EJS >= 1
        assert isinstance(EXTRAIR_IMAGENS, bool)

    def test_gemini_api_key(self):
        """Verifica configuração da API key do Gemini"""
        from scripts.config_ej import GEMINI_API_KEY
        
        # A API key pode ser a padrão ou uma chave real
        assert GEMINI_API_KEY is not None
        assert isinstance(GEMINI_API_KEY, str)
        
        # Se não for a chave padrão, deve ter um formato razoável
        if GEMINI_API_KEY != 'sua_chave_aqui':
            assert len(GEMINI_API_KEY) > 10

    @patch('scripts.config_ej.os.getenv')
    def test_gemini_api_key_ambiente(self, mock_getenv):
        """Testa carregamento da API key do ambiente"""
        mock_getenv.return_value = 'test-key-from-env'
        
        # Recarrega o módulo para aplicar o mock
        import importlib
        import scripts.config_ej
        importlib.reload(scripts.config_ej)
        
        assert scripts.config_ej.GEMINI_API_KEY == 'test-key-from-env'

    def test_configuracao_genai(self):
        """Verifica se o Gemini é configurado corretamente"""
        from scripts.config_ej import GEMINI_API_KEY
        
        # A configuração do Gemini deve acontecer apenas se a chave for válida
        if GEMINI_API_KEY and GEMINI_API_KEY != 'sua_chave_aqui':
            
            try:
                import google.generativeai as genai
                
                assert genai is not None
            except ImportError:
                # Gemini não está instalado, mas isso não é um erro de configuração
                pass

    def test_estrutura_caminhos(self):
        """Verifica a estrutura hierárquica dos caminhos"""
        from scripts.config_ej import OUTPUT_DIR, IMAGES_OUTPUT_DIR
        
        # OUTPUT_DIR deve apontar para data/EJs
        assert OUTPUT_DIR.replace('\\', '/').endswith('data/EJs')
        
        # IMAGES_OUTPUT_DIR deve apontar para site/public/images/EJs
        assert IMAGES_OUTPUT_DIR.replace('\\', '/').endswith('site/public/images/EJs')

    def test_criacao_diretorios(self):
        """Testa se os diretórios podem ser criados"""
        from scripts.config_ej import OUTPUT_DIR, IMAGES_OUTPUT_DIR
        
        # Tenta criar os diretórios 
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            os.makedirs(IMAGES_OUTPUT_DIR, exist_ok=True)
            
            # Verifica se os diretórios existem ou podem ser criados
            assert True 
        except Exception as e:
            pytest.fail(f"Erro ao criar diretórios: {e}")