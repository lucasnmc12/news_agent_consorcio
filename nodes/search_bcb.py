from llm_factory import get_llm

llm = get_llm("search")

def search_bcb(state):
    print ( "Buscando informações sobre o Banco Central...")
    prompt = """
    Busque e resuma as notícias mais recentes e relevantes sobre o 
    Banco Central do Brasil, especialmente sobre decisões, regulamentações, 
    mudanças na taxa Selic, ou qualquer outro fato relevante dos últimos dias.
    """
    result = llm.invoke(prompt)
    state["search_bcb"] = result.content
    return state
