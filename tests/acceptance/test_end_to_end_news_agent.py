import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from graph_definition import workflow
from formatacao.salvar_relatorio_pdf import salvar_como_markdown, converter_md_para_html, salvar_pdf
import os


def is_interrupt(state):
    """
    Verifica se o estado atual é uma interrupção (Human in the Loop).
    """
    return isinstance(state, dict) and "human_message" in state


def test_end_to_end_news_agent():
    # 🔥 Estado inicial
    initial_state = {"query": "OpenAI"}

    # 🚀 Compilar o grafo
    app = workflow.compile()

    # 🏃 Executar o fluxo
    state = initial_state

    while True:
        events = list(app.stream(state))
        last_event = events[-1]

        for key, value in last_event.items():
            print(f"[{key}] → {value}")
            state = value

        if is_interrupt(state):
            print("⚠️ O fluxo foi interrompido para revisão humana. Simulando aprovação...")

            estado_atual = state.get("estado_atual", {})

            # 🔥 Se a interrupção não contém o estado atual corretamente, falha o teste com descrição clara
            assert estado_atual, f"⚠️ Estado atual ausente na interrupção: {state}"

            # Simula que o humano revisou e aprovou
            state = {
                **estado_atual,
                "approved": True
            }
            continue  # Continua após "revisão humana simulada"
        else:
            break  # Sai do loop quando o fluxo finaliza

    # ✅ Validações finais após fluxo completo
    assert state is not None
    assert "conteudo" in state, f"❌ Estado final não possui 'conteudo'. Estado retornado: {state}"
    assert isinstance(state["conteudo"], list), "❌ 'conteudo' não é uma lista."
    assert len(state["conteudo"]) > 0, "❌ 'conteudo' está vazio."

    # 📝 Gerar Markdown
    markdown_text = "\n".join([f"- {item}" for item in state["conteudo"]])
    nome_arquivo_md = "relatorio_end_to_end.md"
    salvar_como_markdown(markdown_text, nome_arquivo_md)

    caminho_md = os.path.join("results", "results_md", nome_arquivo_md)
    assert os.path.exists(caminho_md), "❌ Arquivo Markdown não foi criado."

    # 🔄 Converter para HTML
    html_content = converter_md_para_html(nome_arquivo_md)
    assert "<ul>" in html_content or "<p>" in html_content, "❌ HTML gerado não contém tags esperadas."

    # 🗎 Gerar PDF
    nome_arquivo_pdf = "relatorio_end_to_end.pdf"
    salvar_pdf(html_content, nome_arquivo_pdf)

    caminho_pdf = os.path.join("results", "results_pdf", nome_arquivo_pdf)
    assert os.path.exists(caminho_pdf), "❌ Arquivo PDF não foi criado."
    assert os.path.getsize(caminho_pdf) > 0, "❌ Arquivo PDF está vazio."

    print("✅ Teste End-to-End concluído com sucesso e passou totalmente!")
