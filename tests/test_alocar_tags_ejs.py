import pytest
import json
import os
import tempfile
import numpy as np
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

@pytest.fixture(autouse=True)
def setup_gemini_api_key():
    original_env = dict(os.environ)
    os.environ['GEMINI_API_KEY'] = 'test-key-12345'
    yield
    os.environ.clear()
    os.environ.update(original_env)

class TestAlocarTagsEJs:

    def test_carregar_tags_com_embeddings(self):
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
        
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file_path = temp_file.name
                json.dump(tags_data, temp_file)
            
            tags_dict, tags_flat = carregar_tags_com_embeddings(temp_file_path)
            
            assert tags_dict is not None
            assert len(tags_flat) == 1
            assert tags_flat[0]['id'] == 'python'
            assert isinstance(tags_flat[0]['embedding'], np.ndarray)
            
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_carregar_empresas_juniores(self):
        from scripts.alocar_tags_ejs import carregar_empresas_juniores
        
        ej_data = {
            "empresas_juniores": [
                {"id": "1", "Nome": "Empresa A", "Cursos": "Engenharia"},
                {"id": "2", "Nome": "Empresa B", "Cursos": "Computação"}
            ]
        }
        
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
        from scripts.alocar_tags_ejs import similaridade_cosseno
        
        vec1 = np.array([1, 0, 0])
        vec2 = np.array([1, 0, 0])
        similarity = similaridade_cosseno(vec1, vec2)
        assert abs(similarity - 1.0) < 1e-10
        
        vec3 = np.array([1, 0, 0])
        vec4 = np.array([0, 1, 0])
        similarity = similaridade_cosseno(vec3, vec4)
        assert abs(similarity - 0.0) < 1e-10
        
        vec5 = np.array([0, 0, 0])
        vec6 = np.array([1, 0, 0])
        similarity = similaridade_cosseno(vec5, vec6)
        assert similarity == 0.0

    def test_filtrar_tags_por_curso_tecnico(self):
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
        
        cursos = "Engenharia de Software"
        tags_filtradas = filtrar_tags_por_curso(tags_flat, cursos)
        
        assert len(tags_filtradas) == 2
        assert all(tag['id'] != 'equipe_competicao' for tag in tags_filtradas)

    def test_filtrar_tags_por_curso_nao_tecnico(self):
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
        
        cursos = "Administração"
        tags_filtradas = filtrar_tags_por_curso(tags_flat, cursos)
        
        assert len(tags_filtradas) == 2
        assert all(tag['categoria'] in [
            'Habilidades Interpessoais (Soft Skills)',
            'Tipo de Oportunidade e Foco de Atuação'
        ] for tag in tags_filtradas)

    @patch('scripts.alocar_tags_ejs.genai.embed_content')
    def test_gerar_embedding(self, mock_embed):
        from scripts.alocar_tags_ejs import gerar_embedding
        
        mock_embed.return_value = {'embedding': [0.1, 0.2, 0.3]}
        embedding = gerar_embedding("Texto de teste")
        
        assert isinstance(embedding, np.ndarray)
        mock_embed.assert_called_once()

    @patch('scripts.alocar_tags_ejs.gerar_embedding')
    def test_alocar_tags_por_similaridade(self, mock_gerar_embedding):
        from scripts.alocar_tags_ejs import alocar_tags_por_similaridade
        
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
                'embedding': np.array([0.1, 0.2, 0.3])
            },
            {
                'id': 'java',
                'label': 'Java', 
                'description': 'Linguagem Java',
                'categoria': 'Tecnologia',
                'subcategoria': 'Linguagens',
                'embedding': np.array([0.9, 0.8, 0.7])
            }
        ]
        
        tags_selecionadas = alocar_tags_por_similaridade(
            empresa, tags_flat, threshold=0.9, max_tags=5
        )
        
        assert len(tags_selecionadas) == 1
        assert tags_selecionadas[0]['id'] == 'python'
        assert tags_selecionadas[0]['score'] >= 0.9

    @patch('scripts.alocar_tags_ejs.gerar_embedding')
    def test_alocar_tags_por_similaridade_sem_match(self, mock_gerar_embedding):
        from scripts.alocar_tags_ejs import alocar_tags_por_similaridade
        
        mock_gerar_embedding.return_value = np.array([0.1, 0.1, 0.1])
        
        empresa = {"Nome": "EJ", "Cursos": "Engenharia"}
        tags_flat = [{
            'id': 'tag1', 
            'categoria': 'Geral', 
            'embedding': np.array([-0.9, -0.9, -0.9])
        }]
        
        tags_selecionadas = alocar_tags_por_similaridade(
            empresa, tags_flat, threshold=0.99
        )
        
        assert len(tags_selecionadas) == 0

    @patch.dict('os.environ', {}, clear=True)
    def test_alocar_tags_sem_api_key(self):
        import importlib
        import scripts.alocar_tags_ejs
        
        if 'scripts.alocar_tags_ejs' in sys.modules:
            del sys.modules['scripts.alocar_tags_ejs']
        
        import scripts.alocar_tags_ejs as modulo_recarregado
        importlib.reload(modulo_recarregado)
        
        assert modulo_recarregado.GEMINI_API_KEY is None

    @patch('scripts.alocar_tags_ejs.gerar_embedding')
    def test_alocar_tags_por_similaridade_multiplas_tags(self, mock_gerar_embedding):
        from scripts.alocar_tags_ejs import alocar_tags_por_similaridade
        
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
                'embedding': np.array([0.1, 0.2, 0.3])
            },
            {
                'id': 'java',
                'label': 'Java', 
                'description': 'Linguagem Java',
                'categoria': 'Tecnologia',
                'subcategoria': 'Linguagens',
                'embedding': np.array([0.1, 0.2, 0.3])
            }
        ]
        
        tags_selecionadas = alocar_tags_por_similaridade(
            empresa, tags_flat, threshold=0.5, max_tags=5
        )
        
        assert len(tags_selecionadas) == 2
        assert all(tag['score'] >= 0.5 for tag in tags_selecionadas)

    @patch('scripts.alocar_tags_ejs.os.path.exists')
    @patch('scripts.alocar_tags_ejs.carregar_tags_com_embeddings')
    @patch('scripts.alocar_tags_ejs.carregar_empresas_juniores')
    @patch('scripts.alocar_tags_ejs.alocar_tags_por_similaridade')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_main_sucesso(self, mock_json_dump, mock_open_file, mock_alocar, mock_load_ejs, mock_load_tags, mock_exists):
        from scripts.alocar_tags_ejs import main
        
        mock_exists.return_value = True
        mock_load_tags.return_value = ({}, [{'id': 'tag1'}])
        mock_load_ejs.return_value = [{'Nome': 'EJ 1'}]
        mock_alocar.return_value = [{'id': 'tag1', 'label': 'Tag 1', 'score': 0.9}]
        
        main()
        
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        dados_salvos = args[0]
        assert dados_salvos['total_empresas'] == 1
        assert dados_salvos['empresas_juniores'][0]['Nome'] == 'EJ 1'

    @patch('scripts.alocar_tags_ejs.os.path.exists')
    def test_main_arquivo_tags_inexistente(self, mock_exists):
        from scripts.alocar_tags_ejs import main
        
        # Simula tags.json não existindo (primeira chamada)
        mock_exists.side_effect = [False, True] 
        
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called()
            # Verifica se imprimiu erro
            assert any("ERRO" in str(call) for call in mock_print.mock_calls)

    @patch('scripts.alocar_tags_ejs.os.path.exists')
    def test_main_arquivo_ejs_inexistente(self, mock_exists):
        from scripts.alocar_tags_ejs import main
        
        # Simula tags.json existindo, mas ejs.json não
        mock_exists.side_effect = [True, False] 
        
        with patch('builtins.print') as mock_print:
            main()
            assert any("ERRO" in str(call) for call in mock_print.mock_calls)