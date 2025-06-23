from nodes.search_bcb import search_bcb
from nodes.search_consorcios import search_consorcios
from nodes.search_macro import search_macro
#from nodes.search_generic import search_generic

def search_all(state):
    
    #generic = search_generic(state)
    bcb = search_bcb(state)
    consorcios = search_consorcios(state)
    macro = search_macro(state)

    state["search_bcb"] = bcb["search_bcb"]
    state["search_consorcios"] = consorcios["search_consorcios"]
    state["search_macro"] = macro["search_macro"]
    #state["search_generic"] = generic["search_generic"]


    return state