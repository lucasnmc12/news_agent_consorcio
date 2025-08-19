import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

if not os.getenv("SERPER_API_KEY"):
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

    # 🚩 Verifica se a API Key existe
    if not SERPER_API_KEY:
        print("⚠️ SERPER_API_KEY não configurada no .env ou incorreta.")
        return []

# 🔍 Inclui termos para foco no Brasil e em notícias oficiais
    query_final = (
        f"{query} "
        f"(normativa OR regulamentação OR resolução OR comunicado OR decisão) "
        f"site:g1.globo.com OR site:estadao.com.br OR site:valor.globo.com "
        f"OR site:oglobo.globo.com OR site:exame.com OR site:cnnbrasil.com.br "
        f"OR site:abac.org.br "
        f"OR site:bcb.gov.br/noticias"
        # f"{datetime.now().strftime('%B %Y')} Brasil"  ## Filtr de data já aplicado
    )

    url = "https://google.serper.dev/news"

    payload = {
        "q": query_final,
        "gl": "br",       # Geolocalização Brasil
        "hl": "pt-br",  # Idioma português
        "location": "Brazil",
        "tbs": "qdr:w"   # Filtro para notícias da última semana
    }

    payload_json = json.dumps(payload)

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=payload_json)
        response.raise_for_status()
        resultados = response.json().get("news", [])
    except requests.RequestException as e:
        print(f"⚠️ Erro na requisição: {e}")
        return []

    noticias = []
    for item in resultados[:max_results]:
        noticias.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "content_inicio": item.get("snippet"),
            "fonte": item.get("source"),
            "data": item.get("date"),
        })

    return noticias


def formatar_resultados_serper(noticias):
    """Formata a lista de notícias em texto Markdown"""
    resumo = ""
    for n in noticias:
        titulo = n.get("title")
        url = n.get("url")
        data = n.get("data")
        fonte = n.get("fonte")
        trecho = (n.get("content_inicio") or "").strip().replace("\n", " ")
        dominio = url.split("/")[2].replace("www.", "") if url else "Fonte desconhecida"

        resumo += (
            f"- **Fonte**: {dominio}\n"
            f"  **Título**: {titulo}\n"
            f"  **Link**: {url}\n"
            f"  **Data**: {data}\n"
            f"  **Fonte_serper**: {fonte}\n"
            f"  **Início da matéria**: {trecho[:300]}...\n\n"
        )
    return resumo
