
from langgraph.types import interrupt
from langgraph.types import Command
from graph_definition import workflow
from langgraph.checkpoint.memory import InMemorySaver
import json
from formatacao.salvar_relatorio_pdf import salvar_como_markdown, converter_md_para_html, salvar_pdf
from datetime import datetime



checkpointer = InMemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

# Identificador para o fluxo de execução (obrigatório com checkpointer)
config = {"configurable": {"thread_id": "thread-editorial-001"}}

# Captura a query do usuário
# query_usuario = input("📝 Sobre qual tema você quer gerar o relatório? ")

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

# Define nome base com data
data_hoje = datetime.now().strftime("%d-%m-%Y")
nome_md = f"relatorio_{data_hoje}.md"
nome_pdf = f"relatorio_{data_hoje}.pdf"

# 1. Salva conteúdo como Markdown
salvar_como_markdown(conteudo_final, nome_arquivo=nome_md)

# 2. Converte Markdown para HTML
html = converter_md_para_html(nome_arquivo_md=nome_md)

# 3. Salva HTML como PDF
salvar_pdf(html, nome_arquivo=nome_pdf)
