from nodes.search_bcb import search_bcb
from nodes.search_consorcios import search_consorcios
from nodes.search_macro import search_macro

def search_all(state):
    print("Executando todas as buscas...")

    bcb = search_bcb(state)
    consorcios = search_consorcios(state)
    macro = search_macro(state)

    state["search_bcb"] = bcb["search_bcb"]
    state["search_consorcios"] = consorcios["search_consorcios"]
    state["search_macro"] = macro["search_macro"]

    return state