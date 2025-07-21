import streamlit as st
from datetime import datetime
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from graph_definition import workflow
from formatacao.salvar_relatorio_pdf import salvar_como_markdown, converter_md_para_html, salvar_pdf
import os

st.set_page_config(
    page_title="News Agent - Geração de Relatórios",
    page_icon="📰",
    layout="wide"
)

st.title("📰 News Agent - Geração de Relatórios")

# 1. TELA INICIAL
data_hoje = datetime.now().strftime("%d/%m/%Y")
st.write(f"**Data de hoje:** {data_hoje}")

if "start" not in st.session_state:
    st.session_state.start = False

if st.button("▶️ Iniciar Geração do Relatório", type="primary"):
    st.session_state.start = True

# 2. LÓGICA DE EXECUÇÃO DO GRAFO
if st.session_state.start:
    # Inicializa o grafo e o estado na primeira execução
    if "graph" not in st.session_state:
        st.session_state.checkpointer = InMemorySaver()
        st.session_state.graph = workflow.compile(checkpointer=st.session_state.checkpointer)
        st.session_state.config = {"configurable": {"thread_id": "thread-editorial-streamlit-001"}}
        st.session_state.state = {}

        # 🚀 Executa o grafo pela primeira vez
        with st.spinner("🔎 Buscando notícias e gerando pré-relatório..."):
            st.session_state.state = st.session_state.graph.invoke(st.session_state.state, st.session_state.config)
        st.rerun()

    # Condicional principal: o grafo está interrompido para revisão ou finalizado?
    if "__interrupt__" in st.session_state.state:
        # --- ESTADO DE REVISÃO ---
        interrupt_data = st.session_state.state.get("__interrupt__")[0].value
        estado_atual = interrupt_data.get("estado_atual", {})

        st.subheader("🔍 Notícias Recuperadas")
        tab_macro, tab_consorcios, tab_bcb = st.tabs(["Macroeconomia", "Consórcios", "Banco Central"])
        with tab_macro:
            st.markdown(estado_atual.get("search_macro", "Nenhuma notícia encontrada."))
        with tab_consorcios:
            st.markdown(estado_atual.get("search_consorcios", "Nenhuma notícia encontrada."))
        with tab_bcb:
            st.markdown(estado_atual.get("search_bcb", "Nenhuma notícia encontrada."))

        st.divider()
        st.subheader("📝 Pré-Relatório para Revisão")
        merged_content = estado_atual.get("merged_content", "[Não foi possível gerar o pré-relatório]")
        st.markdown(merged_content)

        st.divider()
        feedback = st.text_area("Feedback", placeholder="Insira os ajustes...", height=150, label_visibility="collapsed")

        resume_data = interrupt_data["estado_atual"]
        col1, col2, _ = st.columns([0.2, 0.25, 0.55])

        with col1:
            if st.button("✅ Aprovar", type="primary"):
                resume_data["approved"] = True
                with st.spinner("Gerando versão final..."):
                    st.session_state.state = st.session_state.graph.invoke(Command(resume=resume_data), st.session_state.config)
                st.rerun()

        with col2:
            if st.button("🔄 Enviar Feedback"):
                if not feedback:
                    st.warning("Por favor, insira um feedback.")
                else:
                    resume_data["approved"] = False
                    resume_data["feedback"] = feedback
                    with st.spinner("Processando feedback..."):
                        st.session_state.state = st.session_state.graph.invoke(Command(resume=resume_data), st.session_state.config)
                    st.rerun()
    else:
        # --- ESTADO FINALIZADO ---
        st.success("Relatório gerado e aprovado com sucesso!")
        conteudo_final = st.session_state.state.get("final_editorial", "⚠️ Nenhum conteúdo final encontrado.")

        st.subheader("📄 Relatório Final")
        st.markdown(conteudo_final)

        data_hoje_file = datetime.now().strftime("%d-%m-%Y")
        nome_md = f"relatorio_{data_hoje_file}.md"
        nome_pdf = f"relatorio_{data_hoje_file}.pdf"

        salvar_como_markdown(conteudo_final, nome_arquivo=nome_md)
        html = converter_md_para_html(nome_arquivo_md=nome_md)
        salvar_pdf(html, nome_arquivo=nome_pdf)

        st.divider()
        caminho_pdf = os.path.join("results", "results_pdf", nome_pdf)
        with open(caminho_pdf, "rb") as f:
            st.download_button("📥 Baixar PDF", f, file_name=nome_pdf.split('/')[-1], mime="application/pdf")