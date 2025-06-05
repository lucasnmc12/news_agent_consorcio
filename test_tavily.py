from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv
import os
from llm_factory import get_llm  # Certifique-se de que isso funciona

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(TAVILY_API_KEY)

def buscar_noticias(query="Banco Central do Brasil últimas notícias"):
    print("🔎 Buscando com Tavily...")
    resultados = tavily_client.search(
        query=query,
        max_results=5,
        time_range="week",
        topic="general",
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

def gerar_relatorio_llm():
    noticias = buscar_noticias()
    if not noticias:
        print("⚠️ Nenhuma notícia encontrada.")
        return

    resumo_links = formatar_resultados(noticias)
    data_execucao = datetime.now().strftime("%d/%m/%Y")

    prompt = f"""
Data de execução do relatório: {data_execucao}

Você é um analista econômico responsável por elaborar relatórios informativos para a diretoria de uma empresa de consórcios.

Com base nas notícias reais a seguir sobre o **Banco Central do Brasil**, elabore um relatório profissional:

{resumo_links}

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
    print("\n📄 Relatório gerado pela LLM:\n")
    print(result.content)

if __name__ == "__main__":
    gerar_relatorio_llm()
