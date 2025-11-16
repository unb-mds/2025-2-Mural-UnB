import pytest
import json
import csv
import numpy as np 

import scripts.alocar_tags_embeddings
from scripts.alocar_tags_embeddings import (
    main,
    similaridade_cosseno,
    alocar_tags_por_similaridade,
    gerar_embedding,
    carregar_laboratorios,
    carregar_tags_com_embeddings
)


def test_similaridade_cosseno_vetores_identicos():
    """Testa se vetores idênticos retornam similaridade 1.0"""
    v1 = np.array([1, 2, 3])
    v2 = np.array([1, 2, 3])
    # Usamos pytest.approx para lidar com a imprecisão de números de ponto flutuante
    assert similaridade_cosseno(v1, v2) == pytest.approx(1.0)

def test_similaridade_cosseno_vetores_ortogonais():
    """Testa se vetores ortogonais (90 graus) retornam 0.0"""
    v1 = np.array([1, 0, 0])
    v2 = np.array([0, 1, 0])
    assert similaridade_cosseno(v1, v2) == pytest.approx(0.0)

def test_similaridade_cosseno_vetores_opostos():
    """Testa se vetores opostos retornam -1.0"""
    v1 = np.array([1, 2, 3])
    v2 = np.array([-1, -2, -3])
    assert similaridade_cosseno(v1, v2) == pytest.approx(-1.0)

def test_similaridade_cosseno_com_vetor_zero():
    """Testa se um vetor zero retorna 0.0"""
    v1 = np.array([1, 2, 3])
    v2 = np.array([0, 0, 0])
    assert similaridade_cosseno(v1, v2) == pytest.approx(0.0)