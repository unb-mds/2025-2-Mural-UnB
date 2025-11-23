"""
Testes unitários para alocar_tags_ejs.py
"""
import pytest
import json
import os
import tempfile
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Mock da API key do Gemini para evitar o exit()
@pytest.fixture(autouse=True)
def setup_gemini_api_key():
    """Configura a API key do Gemini para todos os testes"""
    original_env = dict(os.environ)
    os.environ['GEMINI_API_KEY'] = 'test-key-12345'
    yield
    os.environ.clear()
    os.environ.update(original_env)


class TestAlocarTagsEJs:
    """Testes para alocação de tags usando embeddings"""

    def test_carregar_tags_com_embeddings(self):
        """Testa carregamento de tags com embeddings"""
        from scripts.alocar_tags_ejs import carregar_tags_com_embeddings
        
        tags_data = {
            "categorias": [
                {
                    "nome_categoria": "Tecnologia",
                    "subcategorias": [
                        {
                            "nome_subcategoria": "Desenvolvimento",
                            "tags": [
                                {
                                    "id": "python",
                                    "label": "Python",
                                    "embedding": [0.1, 0.2, 0.3]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # CORREÇÃO: Usar arquivo temporário de forma segura para Windows
        temp_file_path = None
        try:
            # Criar arquivo temporário manualmente
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file_path = temp_file.name
                json.dump(tags_data, temp_file)
            
            # Fechar o arquivo antes de usar
            tags_dict, tags_flat = carregar_tags_com_embeddings(temp_file_path)
            
            assert tags_dict is not None
            assert len(tags_flat) == 1
            assert tags_flat[0]['id'] == 'python'
            assert isinstance(tags_flat[0]['embedding'], np.ndarray)
            
        finally:
            # CORREÇÃO: Verificar se o arquivo existe antes de tentar excluir
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_carregar_empresas_juniores(self):
        """Testa carregamento de empresas juniores"""
        from scripts.alocar_tags_ejs import carregar_empresas_juniores
        
        ej_data = {
            "empresas_juniores": [
                {"id": "1", "Nome": "Empresa A", "Cursos": "Engenharia"},
                {"id": "2", "Nome": "Empresa B", "Cursos": "Computação"}
            ]
        }
        
        # CORREÇÃO: Usar arquivo temporário de forma segura para Windows
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file_path = temp_file.name
                json.dump(ej_data, temp_file)
            
            empresas = carregar_empresas_juniores(temp_file_path)
            
            assert len(empresas) == 2
            assert empresas[0]['Nome'] == "Empresa A"
            assert empresas[1]['Cursos'] == "Computação"
            
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_similaridade_cosseno(self):
        """Testa cálculo de similaridade de cosseno"""
        from scripts.alocar_tags_ejs import similaridade_cosseno
        
        # Vetores idênticos
        vec1 = np.array([1, 0, 0])
        vec2 = np.array([1, 0, 0])
        similarity = similaridade_cosseno(vec1, vec2)
        assert abs(similarity - 1.0) < 1e-10
        
        # Vetores ortogonais
        vec3 = np.array([1, 0, 0])
        vec4 = np.array([0, 1, 0])
        similarity = similaridade_cosseno(vec3, vec4)
        assert abs(similarity - 0.0) < 1e-10
        
        # Vetor zero
        vec5 = np.array([0, 0, 0])
        vec6 = np.array([1, 0, 0])
        similarity = similaridade_cosseno(vec5, vec6)
        assert similarity == 0.0

    def test_filtrar_tags_por_curso_tecnico(self):
        """Testa filtro de tags para curso técnico"""
        from scripts.alocar_tags_ejs import filtrar_tags_por_curso
        
        tags_flat = [
            {
                'id': 'python',
                'label': 'Python',
                'categoria': 'Tecnologia',
                'embedding': np.array([0.1, 0.2, 0.3])
            },
            {
                'id': 'lideranca',
                'label': 'Liderança', 
                'categoria': 'Habilidades Interpessoais (Soft Skills)',
                'embedding': np.array([0.4, 0.5, 0.6])
            },
            {
                'id': 'equipe_competicao',
                'label': 'Equipe Competição',
                'categoria': 'Competições',
                'embedding': np.array([0.7, 0.8, 0.9])
            }
        ]
        
        # Curso técnico (engenharia)
        cursos = "Engenharia de Software"
        tags_filtradas = filtrar_tags_por_curso(tags_flat, cursos)
        
        # Deve remover apenas equipe_competicao, manter as outras
        assert len(tags_filtradas) == 2
        assert all(tag['id'] != 'equipe_competicao' for tag in tags_filtradas)

    def test_filtrar_tags_por_curso_nao_tecnico(self):
        """Testa filtro de tags para curso não técnico"""
        from scripts.alocar_tags_ejs import filtrar_tags_por_curso
        
        tags_flat = [
            {
                'id': 'python',
                'label': 'Python',
                'categoria': 'Tecnologia',
                'embedding': np.array([0.1, 0.2, 0.3])
            },
            {
                'id': 'lideranca',
                'label': 'Liderança',
                'categoria': 'Habilidades Interpessoais (Soft Skills)', 
                'embedding': np.array([0.4, 0.5, 0.6])
            },
            {
                'id': 'consultoria',
                'label': 'Consultoria',
                'categoria': 'Tipo de Oportunidade e Foco de Atuação',
                'embedding': np.array([0.7, 0.8, 0.9])
            }
        ]
        
        # Curso não técnico
        cursos = "Administração"
        tags_filtradas = filtrar_tags_por_curso(tags_flat, cursos)
        
        # Deve manter apenas soft skills e tipo de oportunidade
        assert len(tags_filtradas) == 2
        assert all(tag['categoria'] in [
            'Habilidades Interpessoais (Soft Skills)',
            'Tipo de Oportunidade e Foco de Atuação'
        ] for tag in tags_filtradas)

    @patch('scripts.alocar_tags_ejs.genai.embed_content')
    def test_gerar_embedding(self, mock_embed):
        """Testa geração de embedding"""
        from scripts.alocar_tags_ejs import gerar_embedding
        
        mock_embed.return_value = {'embedding': [0.1, 0.2, 0.3]}
        
        embedding = gerar_embedding("Texto de teste")
        
        assert isinstance(embedding, np.ndarray)
        mock_embed.assert_called_once()

    @patch('scripts.alocar_tags_ejs.gerar_embedding')
    def test_alocar_tags_por_similaridade(self, mock_gerar_embedding):
        """Testa alocação de tags por similaridade"""
        from scripts.alocar_tags_ejs import alocar_tags_por_similaridade
        
        # Mock do embedding gerado
        mock_gerar_embedding.return_value = np.array([0.1, 0.2, 0.3])
        
        empresa = {
            "Nome": "Empresa Teste",
            "Cursos": "Engenharia",
            "Sobre": "Empresa de consultoria",
            "Servicos": "Desenvolvimento web"
        }
        
        tags_flat = [
            {
                'id': 'python',
                'label': 'Python',
                'description': 'Linguagem Python',
                'categoria': 'Tecnologia',
                'subcategoria': 'Linguagens',
                'embedding': np.array([0.1, 0.2, 0.3])  # Similaridade = 1.0
            },
            {
                'id': 'java',
                'label': 'Java', 
                'description': 'Linguagem Java',
                'categoria': 'Tecnologia',
                'subcategoria': 'Linguagens',
                'embedding': np.array([0.9, 0.8, 0.7])  # Similaridade baixa (mas ainda acima do threshold)
            }
        ]
        
        # Aumentar o threshold para selecionar apenas uma tag
        tags_selecionadas = alocar_tags_por_similaridade(
            empresa, tags_flat, threshold=0.9, max_tags=5  # Aumentado para 0.9
        )
        
        # selecionar apenas a tag com similaridade muito alta
        assert len(tags_selecionadas) == 1
        assert tags_selecionadas[0]['id'] == 'python'
        assert tags_selecionadas[0]['score'] >= 0.9

    @patch.dict('os.environ', {}, clear=True)
    def test_alocar_tags_sem_api_key(self):
        """Testa comportamento quando não há API key"""
        # Recarregar o módulo após limpar as variáveis de ambiente
        import importlib
        import scripts.alocar_tags_ejs
        
        # Limpar o cache do módulo para forçar recarregamento
        if 'scripts.alocar_tags_ejs' in sys.modules:
            del sys.modules['scripts.alocar_tags_ejs']
        
        # Recarregar o módulo com ambiente limpo
        import scripts.alocar_tags_ejs as modulo_recarregado
        importlib.reload(modulo_recarregado)
        
        # Verificar se a API key é None após recarregar
        assert modulo_recarregado.GEMINI_API_KEY is None

    #teste para verificar múltiplas tags selecionadas
    @patch('scripts.alocar_tags_ejs.gerar_embedding')
    def test_alocar_tags_por_similaridade_multiplas_tags(self, mock_gerar_embedding):
        """Testa alocação de tags quando múltiplas tags têm alta similaridade"""
        from scripts.alocar_tags_ejs import alocar_tags_por_similaridade
        
        # Mock do embedding gerado
        mock_gerar_embedding.return_value = np.array([0.1, 0.2, 0.3])
        
        empresa = {
            "Nome": "Empresa Teste",
            "Cursos": "Engenharia",
            "Sobre": "Empresa de consultoria",
            "Servicos": "Desenvolvimento web"
        }
        
        tags_flat = [
            {
                'id': 'python',
                'label': 'Python',
                'description': 'Linguagem Python',
                'categoria': 'Tecnologia',
                'subcategoria': 'Linguagens',
                'embedding': np.array([0.1, 0.2, 0.3])  # Similaridade = 1.0
            },
            {
                'id': 'java',
                'label': 'Java', 
                'description': 'Linguagem Java',
                'categoria': 'Tecnologia',
                'subcategoria': 'Linguagens',
                'embedding': np.array([0.1, 0.2, 0.3])  # Mesmo embedding = mesma similaridade
            }
        ]
        
        tags_selecionadas = alocar_tags_por_similaridade(
            empresa, tags_flat, threshold=0.5, max_tags=5
        )
        
        # Ambas as tags devem ser selecionadas pois têm a mesma similaridade alta
        assert len(tags_selecionadas) == 2
        assert all(tag['score'] >= 0.5 for tag in tags_selecionadas)