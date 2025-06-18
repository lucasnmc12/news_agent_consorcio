from duckduckgo_search import DDGS
from datetime import datetime


def buscar_noticias(query, max_results=7):
    """Faz uma busca no DuckDuckGo"""
    resultados = []
    with DDGS() as ddgs:
        search_results = ddgs.text(
            f"{query} notícias {datetime.now().strftime('%Y-%m')}",
            max_results=max_results
        )

        for r in search_results:
            resultados.append({
                "title": r.get("title"),
                "url": r.get("href"),
                "content": r.get("body"),
                "published_date": None,
                "score": None
            })

    return resultados


def formatar_resultados(noticias):
    """Formata a lista de notícias em texto Markdown"""
    resumo = ""
    for n in noticias:
        titulo = n.get("title")
        url = n.get("url")
        trecho = (n.get("content") or "").strip().replace("\n", " ")
        data = n.get("published_date") or "Data não disponível"
        dominio = url.split("/")[2].replace("www.", "") if url else "Fonte desconhecida"
        score = n.get("score") or "Score não disponível"

        resumo += (
            f"- **Fonte**: {dominio}\n"
            f"  **Título**: {titulo}\n"
            f"  **Link**: {url}\n"
            f"  **Resumo**: {trecho[:300]}...\n\n"
            f"  **Data**: {data}\n"
            f"  **Score**: {score}\n\n"
        )
    return resumo
