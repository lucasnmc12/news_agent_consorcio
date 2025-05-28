from llm_factory import get_llm

llm = get_llm("search")

def search_macro(state):
    print("Buscando notícias macroeconômicas...")
    prompt = """
    Busque e resuma as principais notícias macroeconômicas dos últimos dias, 
    focando em fatores que impactam o sistema financeiro, o Banco Central e 
    o mercado de consórcios no Brasil, como inflação, PIB, desemprego ou política monetária.
    """
    result = llm.invoke(prompt)
    state["search_macro"] = result.content
    return state