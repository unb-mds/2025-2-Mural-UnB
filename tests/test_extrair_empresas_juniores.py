"""
Testes unitários para extrair_empresas_juniores.py
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_configurar_ambiente_sucesso(mocker):
    """Testa configuração bem-sucedida do ambiente"""
    # Mock das operações de arquivo
    mocker.patch('os.path.exists', return_value=False)
    mocker.patch('os.makedirs')
    
    # Import dentro do contexto
    from scripts.extrair_empresas_juniores import configurar_ambiente
    
    # Mock da API key configurada
    with patch('scripts.extrair_empresas_juniores.GEMINI_API_KEY', 'chave-valida'):
        resultado = configurar_ambiente()
        
        assert resultado is True

def test_configurar_ambiente_api_key_nao_configurada(mocker):
    """Testa quando API_KEY não está configurada"""
    # Mock da API key não configurada (valor padrão)
    with patch('scripts.extrair_empresas_juniores.GEMINI_API_KEY', 'sua_chave_api_aqui'):
        from scripts.extrair_empresas_juniores import configurar_ambiente
        
        mocker.patch('os.path.exists', return_value=False)
        mocker.patch('os.makedirs')
        
        resultado = configurar_ambiente()
        
        # O código retorna False quando a API key não está configurada
        assert resultado is False

def test_consolidar_dados_empresas(mocker):
    """Testa consolidação de dados removendo duplicatas"""
    from scripts.extrair_empresas_juniores import consolidar_dados_empresas
    
    dados_teste = [
        {"Nome": "Empresa A", "Cursos": "Engenharia"},
        {"Nome": "Empresa A", "Cursos": "Engenharia"},  # Duplicata
        {"Nome": "Empresa B", "Cursos": "Computação"}
    ]
    
    mock_open_file = mocker.patch('builtins.open', mock_open())
    mock_json_dump = mocker.patch('json.dump')
    
    consolidar_dados_empresas(dados_teste, "saida_teste.json")
    
    # Verifica se json.dump foi chamado
    assert mock_json_dump.called
    
    # Pega os argumentos com que json.dump foi chamado
    call_args = mock_json_dump.call_args
    if call_args:
        dados_salvos = call_args[0][0]  # Primeiro argumento de json.dump
        
        # Verifica a estrutura esperada
        assert "metadados" in dados_salvos
        assert "empresas_juniores" in dados_salvos
        assert dados_salvos["metadados"]["total_empresas_unicas"] == 2  
        assert len(dados_salvos["empresas_juniores"]) == 2

def test_mostrar_estatisticas_finais(capsys):
    """Testa exibição de estatísticas finais"""
    from scripts.extrair_empresas_juniores import mostrar_estatisticas_finais
    
    dados_teste = [
        {"Nome": "Empresa A", "Cursos": "Engenharia", "Servicos": "Consultoria"},
        {"Nome": "Empresa B", "Cursos": "Computação", "Servicos": "Desenvolvimento"}
    ]
    
    mostrar_estatisticas_finais(dados_teste)
    
    captured = capsys.readouterr()
    
    assert "PROCESSAMENTO CONCLUÍDO" in captured.out
    assert "Total de empresas juniores" in captured.out
    assert "ESTATÍSTICAS POR CAMPO" in captured.out

def test_mostrar_estatisticas_sem_dados(capsys):
    """Testa estatísticas quando não há dados"""
    from scripts.extrair_empresas_juniores import mostrar_estatisticas_finais
    
    mostrar_estatisticas_finais([])
    
    captured = capsys.readouterr()
    assert "Nenhuma empresa foi extraída" in captured.out

def test_processar_pdf_empresas_juniores_pdf_existente(mocker):
    """Testa processamento quando PDF já existe"""
    from scripts.extrair_empresas_juniores import processar_pdf_empresas_juniores
    
    # Mock do processador
    mock_processor = MagicMock()
    mock_processor.processar_pdf_paginado.return_value = [
        {"Nome": "Empresa Teste", "Cursos": "Engenharia"}
    ]
    
    # Mock para simular que o PDF já existe
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('os.makedirs')
    
    # Mock das configurações necessárias
    with patch('scripts.extrair_empresas_juniores.OUTPUT_DIR', '/fake/dir'), \
         patch('scripts.extrair_empresas_juniores.OUTPUT_JSON', 'test.json'), \
         patch('scripts.extrair_empresas_juniores.EXTRAIR_IMAGENS', False):
        
        resultado = processar_pdf_empresas_juniores(
            mock_processor, 
            "http://url-fake.com/pdf.pdf"
        )
    
    assert len(resultado) == 1
    mock_processor.processar_pdf_paginado.assert_called_once()

def test_processar_pdf_empresas_juniores_pdf_inexistente(mocker):
    """Testa processamento quando PDF precisa ser baixado"""
    from scripts.extrair_empresas_juniores import processar_pdf_empresas_juniores
    
    mock_processor = MagicMock()
    mock_processor.baixar_pdf_direto.return_value = "/caminho/arquivo.pdf"
    mock_processor.processar_pdf_paginado.return_value = []
    
    # Simula: PDF não existe, mas depois o diretório existe
    mocker.patch('os.path.exists', side_effect=[False, True])
    mocker.patch('os.makedirs')
    
    # Mock das configurações
    with patch('scripts.extrair_empresas_juniores.OUTPUT_DIR', '/fake/dir'), \
         patch('scripts.extrair_empresas_juniores.OUTPUT_JSON', 'test.json'), \
         patch('scripts.extrair_empresas_juniores.EXTRAIR_IMAGENS', False):
        
        resultado = processar_pdf_empresas_juniores(
            mock_processor,
            "http://url-fake.com/pdf.pdf" 
        )
    
    mock_processor.baixar_pdf_direto.assert_called_once()
    assert resultado == []

def test_main_integracao(mocker, capsys):
    """Teste de integração da função main"""
    from scripts.extrair_empresas_juniores import main
    
    # Mock de todas as dependências
    mocker.patch('scripts.extrair_empresas_juniores.configurar_ambiente', return_value=True)
    
    # Mock do processador
    mock_processor = MagicMock()
    mocker.patch('scripts.extrair_empresas_juniores.PDFProcessorEJs', return_value=mock_processor)
    
    # Mock do processamento do PDF
    mocker.patch('scripts.extrair_empresas_juniores.processar_pdf_empresas_juniores', return_value=[])
    
    # Mock das funções de consolidação e estatísticas
    mocker.patch('scripts.extrair_empresas_juniores.consolidar_dados_empresas')
    mocker.patch('scripts.extrair_empresas_juniores.mostrar_estatisticas_finais')
    
    main()
    
    captured = capsys.readouterr()
    assert "EXTRATOR DE EMPRESAS JUNIORES UNB" in captured.out

def test_consolidar_dados_sem_empresas(mocker, capsys):  
    """Testa consolidação quando não há dados"""
    from scripts.extrair_empresas_juniores import consolidar_dados_empresas
    
    mock_open_file = mocker.patch('builtins.open', mock_open())
    mock_json_dump = mocker.patch('json.dump')
    
    consolidar_dados_empresas([], "saida_vazia.json")
    
    captured = capsys.readouterr()  
    assert "Nenhum dado para consolidar" in captured.out