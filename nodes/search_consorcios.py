from llm_factory import get_llm
from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(TAVILY_API_KEY)
llm = get_llm("search")

def buscar_noticias_consorcios(query="mercado de consórcios Brasil crescimento regulamentação fraudes fusões ABAC "):
    print("🔎 Buscando notícias sobre consórcios com Tavily...")
    resultados = tavily_client.search(
        query=query,
        max_results=10,
        topic="news",
        days=20,
        include_domains=[
        "valor.globo.com",
        "exame.com",
        "economia.estadao.com.br",
        "g1.globo.com",
        "cnnbrasil.com.br",
        "infomoney.com.br",
        "folha.uol.com.br",
        "oglobo.globo.com",
        "economia.uol.com.br",
        "bcb.gov.br",
        "abac.org.br",
        "ibge.gov.br",
        "ibre.fgv.br",
        "https://abac.org.br/imprensa/press-releases",
        "https://abac.org.br/imprensa/consorcio-na-midia-todos"
    ],
        include_images=False,
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
        resumo += (
            f"- **Fonte**: {dominio}\n"
            f"  **Título**: {titulo}\n"
            f"  **Link**: {url}\n"
            f"  **Resumo**: {trecho[:300]}...\n\n"
        )
    return resumo

def search_consorcios(state):
    noticias = buscar_noticias_consorcios()
    if not noticias:
        print("⚠️ Nenhuma notícia encontrada.")
        return state

    resumo_links = formatar_resultados(noticias)
    data_execucao = datetime.now().strftime("%d/%m/%Y")

    prompt = f"""
Data de execução do relatório: {data_execucao}
Você é um analista econômico responsável por elaborar relatórios para a diretoria de uma empresa do setor de consórcios.

Busque e resuma detalhadamente **as notícias mais recentes (publicadas nos últimos 15 dias)** sobre o **mercado de consórcios no Brasil**.

Dê foco especial a tendências de crescimento, comportamento dos consumidores, mudanças regulatórias, oportunidades de mercado, fusões/aquisições, fraudes, novas tecnologias e qualquer fator relevante que impacte o setor.

**Requisitos obrigatórios**:
- Informe a **data de publicação** de cada notícia.
- Cite **explicitamente a fonte confiável** da informação (ex: ABAC, Valor Econômico, G1, Estadão, Exame, etc).
- Inclua o **link direto para a notícia original** ao final do relatório, em uma seção chamada **"Fontes e Links"**.
- Apresente os dados de forma clara, objetiva e com linguagem profissional.
- Separe as notícias por tópicos ou subtítulos, se necessário.

**Formato esperado por item**:
- **Data**: DD/MM/AAAA  
- **Fonte**: Nome da fonte  
- **Resumo**: [conteúdo em linguagem formal e acessível]

Evite conteúdos opinativos ou desatualizados.
"""

    result = llm.invoke(prompt)
    state["search_consorcios"] = result.content
    print(result.content)
    return state
