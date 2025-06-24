from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper
from utils.llm_factory import get_llm
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

mes_atual = datetime.now().strftime('%B %Y')  # Junho 2025

def search_generic(state):
    """Busca e gera relatório sobre a query do usuário"""
    query = state.get("user_query")

    if not query:
        mensagem = "❌ Nenhuma query informada para a busca."
        print(mensagem)
        return {"search_generic": mensagem}

    noticias = buscar_noticias_serper(query)

    if not noticias:
        mensagem = f"⚠️ Nenhuma notícia encontrada sobre {query}."
        print(mensagem)
        return {"search_generic": mensagem}

    resumo_links = formatar_resultados_serper(noticias)

    data_execucao = datetime.now().strftime("%d/%m/%Y")


    prompt = f"""
        Data de execução do relatório: {data_execucao}
        Você é um analista econômico responsável por elaborar relatórios para a diretoria de uma empresa do setor de consórcios.

        Com base nas notícias publicadas na última semana sobre o {query}.
        {resumo_links}

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

# Chama o modelo
    llm = get_llm("search")
    result = llm.invoke(prompt)

# Salva no estado
    state["search_generic"] = result.content
    print(result.content)
    return state
