"""
Testes unitários para alocar_tags_ejs.py
"""
import os
import sys
import pytest
import json
import numpy as np
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

@pytest.fixture
def mock_gemini_embedding():
    """Fixture para mock de embeddings do Gemini"""
    with patch('scripts.alocar_tags_ejs.genai.configure') as mock_configure, \
         patch('scripts.alocar_tags_ejs.genai.embed_content') as mock_embed:
        
        mock_embed.return_value = {'embedding': [0.1, 0.2, 0.3]}
        yield mock_embed

def test_carregar_tags_com_embeddings(mocker):
    """Testa carregamento de tags com embeddings"""
    from scripts.alocar_tags_ejs import carregar_tags_com_embeddings
    
    dados_tags = {
        "categorias": [{
            "nome_categoria": "Teste",
            "subcategorias": [{
                "nome_subcategoria": "Subteste",
                "tags": [{
                    "id": "tag1",
                    "label": "Tag 1",
                    "description": "Descrição 1",
                    "embedding": [0.1, 0.2, 0.3]
                }]
            }]
        }]
    }
    
    mock_open_file = mocker.patch('builtins.open', mock_open())
    mocker.patch('json.load', return_value=dados_tags)
    mocker.patch('numpy.array', return_value=np.array([0.1, 0.2, 0.3]))
    
    tags_data, tags_flat = carregar_tags_com_embeddings("caminho_fake.json")
    
    assert len(tags_flat) == 1
    assert tags_flat[0]['id'] == 'tag1'
    assert tags_flat[0]['categoria'] == 'Teste'

def test_carregar_empresas_juniores(mocker):
    """Testa carregamento de empresas juniores"""
    from scripts.alocar_tags_ejs import carregar_empresas_juniores
    
    dados_empresas = {
        "empresas_juniores": [
            {"Nome": "Empresa A", "Cursos": "Engenharia"},
            {"Nome": "Empresa B", "Cursos": "Computação"}
        ]
    }
    
    mock_open_file = mocker.patch('builtins.open', mock_open())
    mocker.patch('json.load', return_value=dados_empresas)
    
    empresas = carregar_empresas_juniores("caminho_fake.json")
    
    assert len(empresas) == 2
    assert empresas[0]["Nome"] == "Empresa A"

def test_gerar_embedding(mock_gemini_embedding):
    """Testa geração de embeddings"""
    from scripts.alocar_tags_ejs import gerar_embedding
    
    embedding = gerar_embedding("Texto para embedding")
    
    assert isinstance(embedding, np.ndarray)
    mock_gemini_embedding.assert_called_once()

def test_similaridade_cosseno():
    """Testa cálculo de similaridade de cosseno"""
    from scripts.alocar_tags_ejs import similaridade_cosseno
    
    # Vetores idênticos
    vec1 = np.array([1, 0])
    vec2 = np.array([1, 0])
    similaridade = similaridade_cosseno(vec1, vec2)
    assert abs(similaridade - 1.0) < 0.001
    
    # Vetores ortogonais
    vec3 = np.array([1, 0])
    vec4 = np.array([0, 1])
    similaridade = similaridade_cosseno(vec3, vec4)
    assert abs(similaridade - 0.0) < 0.001
    
    # Vetor zero
    vec5 = np.array([0, 0])
    similaridade = similaridade_cosseno(vec1, vec5)
    assert similaridade == 0.0

def test_filtrar_tags_por_curso():
    """Testa filtragem de tags por curso"""
    from scripts.alocar_tags_ejs import filtrar_tags_por_curso
    
    tags_teste = [
        {
            'id': 'tag_tecnica',
            'label': 'Tag Técnica',
            'categoria': 'Tecnologia',
            'subcategoria': 'Programação',
            'embedding': np.array([0.1, 0.2])
        },
        {
            'id': 'soft_skill',
            'label': 'Comunicação',
            'categoria': 'Habilidades Interpessoais (Soft Skills)',
            'subcategoria': 'Comunicação',
            'embedding': np.array([0.3, 0.4])
        },
        {
            'id': 'equipe_competicao',
            'label': 'Equipe Competição',
            'categoria': 'Competições',
            'subcategoria': 'Equipes',
            'embedding': np.array([0.5, 0.6])
        }
    ]
    
    # Curso técnico
    tags_filtradas_tecnico = filtrar_tags_por_curso(tags_teste, "Engenharia de Software")
    ids_filtrados_tecnico = [tag['id'] for tag in tags_filtradas_tecnico]
    
    # Deve remover apenas equipe_competicao
    assert 'equipe_competicao' not in ids_filtrados_tecnico
    assert 'tag_tecnica' in ids_filtrados_tecnico
    assert 'soft_skill' in ids_filtrados_tecnico
    
    # Curso não-técnico
    tags_filtradas_nao_tecnico = filtrar_tags_por_curso(tags_teste, "Administração")
    ids_filtrados_nao_tecnico = [tag['id'] for tag in tags_filtradas_nao_tecnico]
    
    # Deve manter apenas soft skills
    assert 'soft_skill' in ids_filtrados_nao_tecnico
    assert 'tag_tecnica' not in ids_filtrados_nao_tecnico
    assert 'equipe_competicao' not in ids_filtrados_nao_tecnico

def test_alocar_tags_por_similaridade(mocker):
    """Testa alocação de tags por similaridade"""
    from scripts.alocar_tags_ejs import alocar_tags_por_similaridade
    
    # Mock da geração de embedding
    mocker.patch('scripts.alocar_tags_ejs.gerar_embedding', 
                 return_value=np.array([0.1, 0.2, 0.3]))
    
    # Mock do filtro de tags
    mocker.patch('scripts.alocar_tags_ejs.filtrar_tags_por_curso', 
                 return_value=[
                     {
                         'id': 'tag1',
                         'label': 'Tag 1',
                         'embedding': np.array([0.1, 0.2, 0.3]),  # Similar
                         'categoria': 'Teste',
                         'subcategoria': 'Subteste'
                     },
                     {
                         'id': 'tag2', 
                         'label': 'Tag 2',
                         'embedding': np.array([0.9, 0.8, 0.7]),  # Não similar
                         'categoria': 'Teste',
                         'subcategoria': 'Subteste'
                     }
                 ])
    
    empresa_teste = {
        "Nome": "Empresa Teste",
        "Cursos": "Engenharia",
        "Sobre": "Descrição da empresa"
    }
    
    tags_flat = [
        {
            'id': 'tag1',
            'label': 'Tag 1',
            'description': 'Descrição 1',
            'embedding': np.array([0.1, 0.2, 0.3]),
            'categoria': 'Teste',
            'subcategoria': 'Subteste'
        }
    ]
    
    tags_selecionadas = alocar_tags_por_similaridade(
        empresa_teste, tags_flat, threshold=0.5, max_tags=5
    )
    
    # Deve encontrar pelo menos uma tag com alta similaridade
    assert len(tags_selecionadas) > 0
    assert 'score' in tags_selecionadas[0]

def test_main_arquivos_inexistentes(mocker, capsys):
    """Testa comportamento quando arquivos não existem"""
    from scripts.alocar_tags_ejs import main
    
    mocker.patch('os.path.exists', return_value=False)
    mocker.patch('sys.exit')  # Para evitar que o teste saia
    
    main()
    
    captured = capsys.readouterr()
    assert "ERRO" in captured.out or "não encontrado" in captured.out