
from langgraph.types import interrupt
from langgraph.types import Command
from graph_definition import workflow
from langgraph.checkpoint.memory import InMemorySaver
import json
from salvar_relatorio_pdf import salvar_como_markdown, converter_md_para_html, salvar_pdf


checkpointer = InMemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

# Identificador para o fluxo de execução (obrigatório com checkpointer)
config = {"configurable": {"thread_id": "thread-editorial-001"}}

# Estado inicial
state = {}

while True:
    state = graph.invoke(state if isinstance(state, dict) else Command(resume=resume_data), config=config)

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
        # print("STATE ATUAL:", state)  --> conferindo como o estado está após a aprovação

        continue
    break



#  Verifica estado final:
conteudo_final = state.get("final_editorial", "⚠️ Nenhum conteúdo final encontrado.")

print("\n✅ Resultado final:")
print(conteudo_final)

salvar_como_markdown(conteudo_final)                      # 1. salva .md
html = converter_md_para_html()                           # 2. converte para HTML
salvar_pdf(html)                                          # 3. salva como PDF
