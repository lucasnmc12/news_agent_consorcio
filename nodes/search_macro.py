from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper
from searcher_gemini import buscar_noticias_gemini
from utils.llm_factory import get_llm
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

mes_atual = datetime.now().strftime('%B %Y')  # Junho 2025

def search_macro(state):
    """Busca e gera relatório sobre a macroecônomia do país"""
    query = " economia inflação juros recessão últimas notícias Brasil"
    noticias = buscar_noticias_serper(query)

    if not noticias:
        print("⚠️ Nenhuma notícia encontrada.")
        return state

    resumo_links = formatar_resultados_serper(noticias)

    data_execucao = datetime.now().strftime("%d/%m/%Y")

    prompt = f"""
        Data de execução do relatório: {data_execucao}
        Você é um analista econômico responsável por elaborar relatórios informativos para a diretoria de uma empresa de consórcios.

        Com base nas notícias publicadas na última semana sobre **indicadores macroeconômicos no Brasil**, elabore um relatório profissional:

        {resumo_links}
        Dê foco especial a indicadores como inflação, PIB, taxa de juros, desemprego e câmbio, bem como decisões de política monetária, projeções econômicas e eventos que possam impactar o sistema financeiro e o setor de consórcios.

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
    state["search_macro"] = result.content
    print(result.content)
    return state
