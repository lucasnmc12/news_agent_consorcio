from langgraph.graph import  END
from langgraph.pregel import Interrupt

def request_review(state):
    print("Revisão pendente.")
    print("\nConteúdo gerado até agora:\n")
    print(state.get("merged_content", "Nenhum conteúdo encontrado"))

     # Se quiser, adiciona um flag no estado:
    state["status"] = "Aguardando revisão humana"

    # Pausa o grafo aguardando aprovação
    return Interrupt(value=state)

    
