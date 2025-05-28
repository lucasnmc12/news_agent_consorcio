from langgraph import StateGraph
from langgraph.pregel import END

from nodes.search_bcb import search_bcb
from nodes.search_consorcios import search_consorcios
from nodes.search_macro import search_macro
from nodes.merge_results import merge_results
from nodes.request_review import request_review
from nodes.review_llm import review_llm
from nodes.format_editorial import format_editorial

GraphState = dict

workflow = StateGraph(GraphState)

# Adiciona os nós
workflow.add_node("search_bcb", search_bcb)
workflow.add_node("search_consorcios", search_consorcios)
workflow.add_node("search_macro", search_macro)
workflow.add_node("merged_content", merge_results)
workflow.add_node("request_review", request_review)
workflow.add_node("review_llm", review_llm)
workflow.add_node("format_editorial", format_editorial)

# Pontos de entrada
workflow.set_entry_point(["search_bcb", "search_consorcios", "search_macro"])

# Transições de busca --> merge
workflow.add_edge("search_bcb", "merged_content")
workflow.add_edge("search_consorcios", "merge_results")
workflow.add_edge("search_macro", "merge_results")

# Merge --> revisão
workflow.add_edge("merged_content", "request_review")

# Decisão após revisão

def review_edge(state):
    if state.get("approved"):
        return "fromat_editorial"
    else:
        return "review_llm"
    
workflow.add_edge("request_review", review_edge)

# Após revisão automática, volta para a revisão manual 
workflow.add_edge("review_llm", "request_review")


# Finalização
workflow.set_finish_point("format_editorial")

# Compila 
graph = workflow.compile()


