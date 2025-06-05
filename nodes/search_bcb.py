from llm_factory import get_llm
from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv() 

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(TAVILY_API_KEY)

def buscar_noticias(query="Banco Central do Brasil inflação taxa de juros Selic comunicados oficiais últimas notícias"):
    print("🔎 Buscando notícias do Banco Central com Tavily...")
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
        data = n.get("published_date")
        dominio = url.split("/")[2].replace("www.", "")
        score = n.get("score")
        resumo += (
            f"- **Fonte**: {dominio}\n"
            f"  **Título**: {titulo}\n"
            f"  **Link**: {url}\n"
            f"  **Resumo**: {trecho[:300]}...\n\n"
            f"  **Data**: {data}\n\n"
            f"  **Score**: {score}\n"
        )
    return resumo

def search_bcb(state):
    noticias = buscar_noticias()
    if not noticias:
        print("⚠️ Nenhuma notícia encontrada.")
        return state

    resumo_links = formatar_resultados(noticias)
    data_execucao = datetime.now().strftime("%d/%m/%Y")

    prompt = f"""
Data de execução do relatório: {data_execucao}

Você é um analista econômico responsável por elaborar relatórios informativos para a diretoria de uma empresa de consórcios.

Com base nas notíciasdos últimos 15 dias sobre o **Banco Central do Brasil**, elabore um relatório profissional:

{resumo_links}

Dê foco especial a decisões, regulamentações, comunicados oficiais, mudanças na **taxa Selic**, projeções econômicas e quaisquer medidas que possam impactar o mercado financeiro ou o setor de consórcios.

**Requisitos obrigatórios**:
- Informe a **data de publicação** de cada notícia.
- Cite **explicitamente a fonte confiável** da informação (ex: Valor Econômico, G1, Estadão, CNN, etc).
- Inclua o **link direto para a notícia original** ao final do relatório, em uma seção chamada **"Fontes e Links"**.
- Apresente os dados de forma clara, objetiva e com linguagem profissional.
- Separe as notícias por tópicos ou subtítulos, se necessário.

**Formato esperado por item**:
- **Data**: DD/MM/AAAA  
- **Fonte**: Nome da fonte  
- **Resumo**: [conteúdo em linguagem formal e acessível]

Evite opiniões pessoais, especulações ou informações desatualizadas.
"""

    llm = get_llm("search")
    result = llm.invoke(prompt)
    state["search_bcb"] = result.content
    return state
