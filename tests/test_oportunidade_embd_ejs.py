"""
Testes unitários para oportunidade_embd_ejs.py
"""
import pytest
import json
import os
import tempfile
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Importar após adicionar ao path
import scripts.oportunidade_embd_ejs as oportunidade_embd_ejs


class TestOportunidadeEmbdEJs:
    """Testes para agregação de embeddings"""

    def test_carregar_lookup_embeddings_sucesso(self):
        """Testa carregamento bem-sucedido do lookup de embeddings"""
        # Cria arquivo JSON de tags temporário
        tags_data = {
            "categorias": [
                {
                    "nome_categoria": "Teste",
                    "subcategorias": [
                        {
                            "nome_subcategoria": "Subteste",
                            "tags": [
                                {
                                    "id": "tag1",
                                    "label": "Tag 1",
                                    "embedding": [0.1, 0.2, 0.3]
                                },
                                {
                                    "id": "tag2", 
                                    "label": "Tag 2",
                                    "embedding": [0.4, 0.5, 0.6]
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
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file_path = temp_file.name
                json.dump(tags_data, temp_file)
            
            # Fechar o arquivo antes de usar
            lookup = oportunidade_embd_ejs.carregar_lookup_embeddings(temp_file_path)
            
            assert lookup is not None
            assert len(lookup) == 2
            assert "tag1" in lookup
            assert "tag2" in lookup
            assert isinstance(lookup["tag1"], list)
            
        finally:
            # CORREÇÃO: Verificar se o arquivo existe antes de tentar excluir
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_carregar_lookup_embeddings_arquivo_nao_encontrado(self):
        """Testa carregamento com arquivo não encontrado"""
        lookup = oportunidade_embd_ejs.carregar_lookup_embeddings("/caminho/inexistente/tags.json")
        assert lookup is None

    def test_carregar_lookup_embeddings_json_invalido(self):
        """Testa carregamento com JSON inválido"""
        # CORREÇÃO: Usar caracteres ASCII para evitar problemas de encoding
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write('{"invalid json"')  # JSON inválido sem caracteres especiais
                temp_file.flush()
            
            # Fechar o arquivo antes de usar
            lookup = oportunidade_embd_ejs.carregar_lookup_embeddings(temp_file_path)
            assert lookup is None
            
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_processar_empresas_juniores_com_embeddings(self):
        """Testa processamento de empresas com embeddings"""
        # Dados de exemplo
        lookup_embeddings = {
            "tag1": [1.0, 2.0, 3.0],
            "tag2": [4.0, 5.0, 6.0]
        }
        
        dados_ejs = {
            "empresas_juniores": [
                {
                    "id": "1",
                    "Nome": "Empresa A",
                    "tags": [{"id": "tag1"}, {"id": "tag2"}]
                },
                {
                    "id": "2", 
                    "Nome": "Empresa B",
                    "tags": [{"id": "tag1"}]
                }
            ]
        }
        
        # CORREÇÃO: Usar arquivo temporário de forma segura
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file_path = temp_file.name
                json.dump(dados_ejs, temp_file)
            
            # Fechar o arquivo antes de usar
            resultado = oportunidade_embd_ejs.processar_empresas_juniores(temp_file_path, lookup_embeddings)
            
            assert resultado is not None
            empresas = resultado.get("empresas_juniores", [])
            assert len(empresas) == 2
            
            # Verifica se os embeddings foram calculados
            assert "embedding_agregado" in empresas[0]
            assert "embedding_agregado" in empresas[1]
            
            # Verifica cálculo do embedding médio
            emb_empresa_a = empresas[0]["embedding_agregado"]
            emb_empresa_b = empresas[1]["embedding_agregado"]
            
            # Empresa A deve ter média de tag1 e tag2
            expected_a = np.mean([lookup_embeddings["tag1"], lookup_embeddings["tag2"]], axis=0)
            np.testing.assert_array_almost_equal(emb_empresa_a, expected_a.tolist())
            
            # Empresa B deve ter apenas tag1
            expected_b = lookup_embeddings["tag1"]
            np.testing.assert_array_almost_equal(emb_empresa_b, expected_b)
                
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_processar_empresas_juniores_sem_tags(self):
        """Testa processamento de empresas sem tags"""
        lookup_embeddings = {"tag1": [1.0, 2.0, 3.0]}
        
        dados_ejs = {
            "empresas_juniores": [
                {
                    "id": "1",
                    "Nome": "Empresa A",
                    "tags": []  # Sem tags
                }
            ]
        }
        
        # CORREÇÃO: Usar arquivo temporário de forma segura
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file_path = temp_file.name
                json.dump(dados_ejs, temp_file)
            
            # Fechar o arquivo antes de usar
            resultado = oportunidade_embd_ejs.processar_empresas_juniores(temp_file_path, lookup_embeddings)
            
            assert resultado is not None
            empresa = resultado["empresas_juniores"][0]
            assert empresa["embedding_agregado"] is None
                
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_processar_empresas_juniores_arquivo_nao_encontrado(self):
        """Testa processamento com arquivo não encontrado"""
        lookup_embeddings = {"tag1": [1.0, 2.0, 3.0]}
        resultado = oportunidade_embd_ejs.processar_empresas_juniores("/caminho/inexistente/ej.json", lookup_embeddings)
        assert resultado is None

    def test_salvar_resultado(self):
        """Testa salvamento do resultado"""
        dados_teste = {
            "empresas_juniores": [
                {"id": "1", "Nome": "Empresa A", "embedding_agregado": [1.0, 2.0, 3.0]}
            ]
        }
        
        # CORREÇÃO: Usar arquivo temporário de forma segura
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file_path = temp_file.name
                json.dump({}, temp_file)  # Arquivo vazio inicialmente
            
            # Fechar o arquivo antes de usar
            oportunidade_embd_ejs.salvar_resultado(dados_teste, temp_file_path)
            
            # Verifica se o arquivo foi criado
            assert os.path.exists(temp_file_path)
            
            # Verifica se o conteúdo está correto
            with open(temp_file_path, 'r', encoding='utf-8') as f:
                dados_salvos = json.load(f)
            
            assert dados_salvos["empresas_juniores"][0]["Nome"] == "Empresa A"
            
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_salvar_resultado_erro_io(self):
        """Testa salvamento com erro de IO"""
        dados_teste = {"teste": "dados"}
        
        # CORREÇÃO: A função salvar_resultado não levanta exceção, apenas imprime erro
        # Vamos testar que ela executa sem crash
        try:
            oportunidade_embd_ejs.salvar_resultado(dados_teste, "/caminho/inexistente/arquivo.json")
            # Se chegou aqui, a função executou sem crash (ela trata o erro internamente)
            assert True
        except Exception as e:
            # Se houver alguma exceção não tratada, o teste falha
            pytest.fail(f"salvar_resultado levantou exceção não tratada: {e}")

    # CORREÇÃO: Adicionar teste para verificar o comportamento de erro
    def test_salvar_resultado_com_erro(self, capsys):
        """Testa que salvar_resultado imprime mensagem de erro quando há problema"""
        dados_teste = {"teste": "dados"}
        
        oportunidade_embd_ejs.salvar_resultado(dados_teste, "/caminho/inexistente/arquivo.json")
        
        captured = capsys.readouterr()
        # Verifica se a mensagem de erro foi impressa
        assert "Erro ao salvar arquivo" in captured.out

    # CORREÇÃO: Adicionar teste para estrutura vazia
    def test_carregar_lookup_embeddings_estrutura_vazia(self):
        """Testa carregamento com estrutura de tags vazia"""
        tags_data = {
            "categorias": []  # Sem categorias
        }
        
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file_path = temp_file.name
                json.dump(tags_data, temp_file)
            
            lookup = oportunidade_embd_ejs.carregar_lookup_embeddings(temp_file_path)
            
            assert lookup is not None
            assert len(lookup) == 0  # Lookup vazio
            
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    # CORREÇÃO: Adicionar teste para tags sem embedding
    def test_carregar_lookup_embeddings_tags_sem_embedding(self):
        """Testa carregamento quando tags não têm embedding"""
        tags_data = {
            "categorias": [
                {
                    "nome_categoria": "Teste",
                    "subcategorias": [
                        {
                            "nome_subcategoria": "Subteste", 
                            "tags": [
                                {
                                    "id": "tag1",
                                    "label": "Tag 1"
                                    # Sem embedding
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
            
            lookup = oportunidade_embd_ejs.carregar_lookup_embeddings(temp_file_path)
            
            assert lookup is not None
            assert len(lookup) == 0  # Tags sem embedding não são incluídas
            
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)