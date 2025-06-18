from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper
from utils.llm_factory import get_llm
from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv() 

mes_atual = datetime.now().strftime('%B %Y')  # Junho 2025

def search_bcb(state):
    """Busca e gera relatório sobre Banco Central"""
    query = """Banco Central do Brasil"""
    noticias = buscar_noticias_serper(query)

    if not noticias:
        print("⚠️ Nenhuma notícia encontrada.")
        return state

    resumo_links = formatar_resultados_serper(noticias)

    data_execucao = datetime.now().strftime("%d/%m/%Y")
    
    prompt = f"""
Data de execução do relatório: {data_execucao}

Você é um analista econômico responsável por elaborar relatórios informativos para a diretoria de uma empresa de consórcios.

Com base nas notícias dos últimos 15 dias sobre o **Banco Central do Brasil**, elabore um relatório profissional:

{resumo_links}

Dê foco especial a decisões, regulamentações, comunicados oficiais, mudanças na **taxa Selic**, projeções econômicas e quaisquer medidas que possam impactar o mercado financeiro ou o setor de consórcios.

**Requisitos obrigatórios**:
        - Cite **explicitamente a fonte confiável** da informação (ex: ABAC, Valor Econômico, G1, Estadão, Exame, etc).
        - Apresente os dados de forma clara, detalhada e com linguagem profissional.
        - Separe as notícias por tópicos ou subtítulos, se necessário.

        **Formato esperado por item**:
        - **Título**: Título da notícia  
        - **Conteúdo**: [conteúdo detalhado em linguagem formal e acessível]
        - **Fonte**: Nome da fonte  
        - **Link**: URL da notícia 

Evite opiniões pessoais, especulações ou informações desatualizadas.
"""

    llm = get_llm("search")
    result = llm.invoke(prompt)
    state["search_bcb"] = result.content
    return state
