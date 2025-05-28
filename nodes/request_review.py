from langgraph import END, StateGraph
from langgraph.pregel import interrupt

def request_review(state):
    print("Revisão pendente.")
    print("\nConteúdo gerado até agora:\n")
    print(state["merged_content"])

    # Pausa o grafo aguardando aprovação
    raise interrupt("Aguardando revisão humana")

    
