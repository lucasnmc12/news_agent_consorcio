import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def buscar_noticias_serper(query, max_results=5):
    """
    Faz uma busca no Google usando a API do Serper.dev com foco no Brasil.

    :param query: Tema da busca
    :param max_results: Quantidade máxima de resultados (máximo 10 na API gratuita)
    :return: Lista de dicionários com título, url e snippet
    """
    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    # 🔍 Inclui termos para foco no Brasil e em notícias oficiais
    query_final = (
        f"{query} "
        f"(normativa OR regulamentação OR resolução OR comunicado OR decisão) "
        f"site:g1.globo.com OR site:estadao.com.br OR site:valor.globo.com "
        f"OR site:oglobo.globo.com OR site:exame.com OR site:cnnbrasil.com.br "
        f"OR site:abac.org.br "
        f"{datetime.now().strftime('%B %Y')} Brasil"
    )

    payload = {
        "q": query_final
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    resultados = response.json().get("organic", [])

    noticias = []
    for item in resultados[:max_results]:
        noticias.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "content": item.get("snippet")
        })

    return noticias


def formatar_resultados_serper(noticias):
    """Formata a lista de notícias em texto Markdown"""
    resumo = ""
    for n in noticias:
        titulo = n.get("title")
        url = n.get("url")
        trecho = (n.get("content") or "").strip().replace("\n", " ")
        dominio = url.split("/")[2].replace("www.", "") if url else "Fonte desconhecida"

        resumo += (
            f"- **Fonte**: {dominio}\n"
            f"  **Título**: {titulo}\n"
            f"  **Link**: {url}\n"
            f"  **Resumo**: {trecho[:300]}...\n\n"
        )
    return resumo
