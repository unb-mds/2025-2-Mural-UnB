"""
Configurações globais para pytest
"""
import os
import sys
import pytest


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configura ambiente de teste para todos os testes"""
    
    original_env = dict(os.environ)
    os.environ['GEMINI_API_KEY'] = 'test-key-12345'
    
    yield
    
    
    os.environ.clear()
    os.environ.update(original_env)