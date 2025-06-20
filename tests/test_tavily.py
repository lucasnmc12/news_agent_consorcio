from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv
import os
from llm_factory import get_llm  # Certifique-se de que isso funciona

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(TAVILY_API_KEY)

def buscar_noticias(query='"consórcio 2025" AND Brasil'):
    print("🔎 Testando com Tavily...")
    resultados = tavily_client.search(
        query=query,
        max_results=10,
        topic="general",
        country = "brazil",
        include_domains = [
            "valor.globo.com",
            "g1.globo.com",
            "economia.estadao.com.br",
            "infomoney.com.br",
            "oglobo.globo.com",
            "economia.uol.com.br"
            "blog.abac.org.br"
        ],
        #days=8, # somente com topic = news
        time_range="day",
        include_images=False,
        include_raw_content=False,
        include_image_descriptions=False,
        search_depth="advanced",
        exclude_domains=["instagram.com"]
    )
    return resultados.get("results", [])


def formatar_resultados(noticias):
    resumo = ""
    for n in noticias:
        titulo = n.get("title")
        url = n.get("url")
        trecho = n.get("content", "").strip().replace("\n", " ")
        dominio = url.split("/")[2].replace("www.", "")
        #data = n.get("published_date")  #  --> somente com topic news
        resumo += (
            f"- **Fonte**: {dominio}\n"
            f"  **Título**: {titulo}\n"
            f"  **Link**: {url}\n"
            f"  **Resumo**: {trecho[:1000]}...\n\n"
            #f"  **Data**: {data}\n"
        )
    return resumo


if __name__ == "__main__":
    noticia = buscar_noticias()
    if noticia:
        print("✅ Resultados obtidos:")
        print(formatar_resultados(noticia))
    else:
        print("❌ Nenhum resultado retornado pela Tavily.")


