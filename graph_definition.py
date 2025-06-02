from langgraph.graph import StateGraph, END
# from langgraph.pregel import END

from nodes.merged_content import merged_content
from nodes.request_review import request_review
from nodes.review_llm import review_llm
from nodes.format_editorial import format_editorial
from nodes.search_all import search_all

from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

GraphState = dict

workflow = StateGraph(GraphState)

# Adiciona os nós
workflow.add_node("search_all", search_all) 
workflow.add_node("merged_content", merged_content)
workflow.add_node("request_review", request_review)
workflow.add_node("review_llm", review_llm)
workflow.add_node("format_editorial", format_editorial)

# Pontos de entrada
workflow.set_entry_point("search_all")

# Transições de busca --> merge

workflow.add_edge("search_all", "merged_content")

# Merge --> revisão
workflow.add_edge("merged_content", "request_review")

# Decisão após revisão

def review_edge(state):
    print("🔎 review_edge recebeu:", state)
    if state.get("approved"):
        return "format_editorial"
    else:
        return "review_llm"
    
workflow.add_conditional_edges("request_review", review_edge)

# Após revisão automática, volta para a revisão manual 
workflow.add_edge("review_llm", "request_review")


# Finalização
workflow.set_finish_point("format_editorial")

# Compila 
graph = workflow.compile(checkpointer=checkpointer)


