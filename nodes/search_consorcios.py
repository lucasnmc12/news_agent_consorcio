from llm_factory import get_llm

llm = get_llm("search")

def search_consorcios(state):
    print("Buscando notícias sobre consórcios...")
    prompt = """
    Busque e resuma notícias atuais sobre o mercado de consórcios no Brasil, 
    incluindo tendências, regulamentações, crescimento, problemas ou oportunidades recentes.
    """
    result = llm.invoke(prompt)
    state["search_consorcios"] = result.content
    return state