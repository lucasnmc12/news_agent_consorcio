from langgraph.graph import StateGraph
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver

def request_review(state):
    print("Revisão pendente.")

    estado_atual = state.copy()
    estado_atual["status"] = "Aguardando revisão humana"

    return interrupt({
        "human_message": "O conteúdo foi interrompido para revisão humana",
        "estado_atual": estado_atual
        })

    

    
