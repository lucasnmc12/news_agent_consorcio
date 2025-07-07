# from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper
from searcher_gemini import buscar_noticias_gemini
from utils.llm_factory import get_llm
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

mes_atual = datetime.now().strftime('%B %Y')  # Junho 2025

def search_consorcios(state):
    """Busca e gera relatório sobre o mercado de consórcios"""
    query = " mercado de consórcios últimas notícias Brasil"

    noticias = buscar_noticias_gemini(query)

    if not noticias:
        mensagem = "⚠️ Nenhuma notícia encontrada sobre consórcios."
        print(mensagem)
        return {"search_consorcios": mensagem}

    resumo_links = noticias

    data_execucao = datetime.now().strftime("%d/%m/%Y")


    prompt = f"""
        Data de execução do relatório: {data_execucao}
        Você é um analista econômico responsável por elaborar relatórios para a diretoria de uma empresa do setor de consórcios.

        Com base nas notícias publicadas na última semana sobre o **mercado de consórcios no Brasil**.
        {resumo_links}

        Dê foco especial a tendências de crescimento, comportamento dos consumidores, mudanças regulatórias, oportunidades de mercado, fusões/aquisições, fraudes, novas tecnologias e qualquer fator relevante que impacte o setor.

        **Requisitos obrigatórios**:
        - Cite **explicitamente a fonte confiável** da informação (ex: ABAC, Valor Econômico, G1, Estadão, Exame, etc).
        - Apresente os dados de forma clara, detalhada e com linguagem profissional.
        - Separe as notícias por tópicos ou subtítulos, se necessário.

        **Formato esperado por item**:
        - **Título**: Título da notícia  
        - **Conteúdo**: [conteúdo detalhado em linguagem formal e acessível]
        - **Fonte**: Nome da fonte  
        - **Link**: URL da notícia 

        Evite conteúdos opinativos ou desatualizados.
        """

    llm = get_llm("search")
    result = llm.invoke(prompt)
    state["search_consorcios"] = result.content
    print(result.content)
    return state
