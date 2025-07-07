from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper
from searcher_gemini import buscar_noticias_gemini
from searcher_gemini import buscar_noticias_gemini
from utils.llm_factory import get_llm
from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv() 

mes_atual = datetime.now().strftime('%B %Y')  # Junho 2025

def search_bcb(state):
    """Busca e gera relatório sobre Banco Central"""
    query = """Banco Central do Brasil últimas notícias"""
    noticias = buscar_noticias_gemini(query)

    if not noticias:
        print("⚠️ Nenhuma notícia encontrada.")
        return state

    resumo_links = noticias

    data_execucao = datetime.now().strftime("%d/%m/%Y")
    
    prompt = f"""
Data de execução do relatório: {data_execucao}

Com base nas notícias publicadas na última semana sobre o **Banco Central do Brasil**, elabore um panorama atualizado sobre o Banco Central do Brasil:
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
