from llm_factory import get_llm
 
llm = get_llm("merge")

def merged_content(state):
    prompt = f"""
    Você é um editor de notícias. Una os seguintes resumos em um único texto editorial, 
    removendo duplicatas, mantendo fluidez, coerência e clareza. Separe por seções 
    se fizer sentido.

    - Banco Central {state.get('search_bcb', '')}
    - Consórcios: {state.get('search_consorcios', '')}
    - Macroeconomia: {state.get('search_macro', '')}
    """

    result = llm.invoke(prompt)
    state ['merged_content'] = result.content
    return state