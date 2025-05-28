from graph_definition import graph
from langgraph.pregel import Interrupt

#  Executa até o primeiro interrupt (após busca e merge)
state = graph.invoke({})

if isinstance(state, Interrupt):
    print("\n Grafo pausou na revisão (request_review)")
    if hasattr(state, "value"):
        state = state.value  #  Extrai o estado atual
    else:
        state = {}
# ✅ Garante que o estado seja um dicionário válido
assert isinstance(state, dict), "O estado deve ser um dicionário!"

print("\n Estado atual (após busca e merge):")
print(state)

#  O grafo agora está pausado na revisão manual (request_review).

# ✅ ➕ Se quiser aprovar:
print("\n✅ Aprovado manualmente, continuando o fluxo...\n")
state = graph.invoke(
    {
        **state, # <-- recebe o estado anterior
        "approved": True,
        "approved_content": "Aprovado. O texto está ótimo!"
    }
)

#   Ou, se quiser solicitar uma revisão automática:
# state = graph.invoke(
#     {
#         "approved": False,
#         "feedback": "Melhore a parte de macroeconomia e adicione dados mais recentes."
#     }
# )

if isinstance(state, Interrupt):
    print("\n Grafo pausou novamente na revisão (após revisão automática)")
    state = state.value  #  Extrai novamente o estado

# ✅ Garante que o estado final seja um dicionário
assert isinstance(state, dict), "O estado final deve ser um dicionário!"

#  Verifica estado final:
print("\n✅ Resultado final:")
print(state.get("final_editorial", "⚠️ Nenhum conteúdo final encontrado."))
