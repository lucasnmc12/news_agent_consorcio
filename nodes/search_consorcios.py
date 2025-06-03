from llm_factory import get_llm
from datetime import datetime


llm = get_llm("search")

def search_consorcios(state):
    print("Buscando notícias sobre consórcios...")
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
    return state