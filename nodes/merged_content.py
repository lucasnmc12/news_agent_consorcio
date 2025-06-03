from llm_factory import get_llm
 
llm = get_llm("merge")

def merged_content(state):
    prompt = f"""
        Você é um editor de notícias que está preparando um relatório executivo para a diretoria de uma empresa de consórcios.

        Sua tarefa é unir os resumos abaixo em um único texto editorial coeso, claro e bem estruturado. Remova duplicações, mantenha a fluidez da leitura e agrupe os conteúdos por temas (ex: Banco Central, Macroeconomia, Consórcios).

        - Banco Central: {state.get('search_bcb', '')}
        - Consórcios: {state.get('search_consorcios', '')}
        - Macroeconomia: {state.get('search_macro', '')}

        **Requisitos obrigatórios**:
        - Mantenha a **data de publicação** de cada notícia mencionada.
        - Cite **explicitamente a fonte confiável** da informação (ex: ABAC, Valor Econômico, G1, Estadão, Exame, etc).
        - Inclua o **link direto para a notícia original** ao final do relatório, em uma seção chamada **"Fontes e Links"**.
        - Apresente o conteúdo de forma clara, objetiva e com linguagem profissional.
        - Separe o texto em seções ou subtítulos conforme o tema de cada bloco (ex: Banco Central, Consórcios, Macroeconomia).
        """

    result = llm.invoke(prompt)
    state ['merged_content'] = result.content
    return state