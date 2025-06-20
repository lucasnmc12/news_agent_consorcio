import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper
import pytest


@pytest.mark.skipif(
    not os.getenv("SERPER_API_KEY"),
    reason="SERPER_API_KEY não configurada no .env"
)
def test_buscar_noticias_serper_retorna_lista():
    resultados = buscar_noticias_serper("Inteligência Artificial", max_results=3)
    assert isinstance(resultados, list)
    assert len(resultados) <= 3

    if resultados:  # Verifica se teve retorno
        for item in resultados:
            assert 'title' in item
            assert 'url' in item
            assert 'content' in item


def test_formatar_resultados_serper():
    noticias_mock = [
        {
            "title": "Notícia 1",
            "url": "https://g1.globo.com/noticia-1",
            "content": "Conteúdo resumido da notícia 1"
        },
        {
            "title": "Notícia 2",
            "url": "https://exame.com/noticia-2",
            "content": "Conteúdo resumido da notícia 2"
        }
    ]

    resultado = formatar_resultados_serper(noticias_mock)

    assert "**Fonte**: g1.globo.com" in resultado
    assert "**Título**: Notícia 1" in resultado
    assert "**Link**: https://g1.globo.com/noticia-1" in resultado
    assert "**Resumo**: Conteúdo resumido da notícia 1" in resultado

    assert "**Fonte**: exame.com" in resultado
    assert "**Título**: Notícia 2" in resultado
