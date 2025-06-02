from graph_definition import graph
from langgraph.types import interrupt
from langgraph.types import Command

# Identificador para o fluxo de execução (obrigatório com checkpointer)
config = {"configurable": {"thread_id": "thread-editorial-001"}}

# Estado inicial
state = {}

while True:
    state = graph.invoke(state if isinstance(state, dict) else Command(resume=state), config=config)


    # 📍 Verifica se houve interrupção para revisão humana
    if "__interrupt__" in state:
        interrupt = state["__interrupt__"][0].value
        print("\nMensagem para humano: ", interrupt["human_message"])

        merged = interrupt["estado_atual"].get("merged_content", "[sem conteúdo]")
        print(f"\nConteúdo atual:\n{merged}")

        resposta_humana = input("\nDigite 'aprovado' ou escreva um feedback personalizado: ")

        resume_data = interrupt["estado_atual"] # recupera o estado atual no momento do interrupt

        if resposta_humana.strip().lower() == "aprovado":
            resume_data["approved"] = True
            resume_data["approved_content"] = "Aprovado manualmente"
        else:
            resume_data["approved"] = False
            resume_data["feedback"] = resposta_humana

        state = Command(resume=resume_data)
        continue
    break

#  Verifica estado final:
print("\n✅ Resultado final:")
print(state.get("final_editorial", "⚠️ Nenhum conteúdo final encontrado."))
