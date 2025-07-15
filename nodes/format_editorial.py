from utils.llm_factory import get_llm

llm = get_llm("formating")

def format_editorial(state):
    print("Formatando o texto para editorial final...")

    merged = state.get('merged_content', '')
    macro = state.get('search_macro', '')
    consorcios = state.get('search_consorcios', '')
    bcb = state.get('search_bcb', '')

    prompt = f"""
            Você é um editor sênior responsável por preparar **relatórios informativos semanais**, voltados ao setor da Controladoria da empresa "Multimarcas Consórcios", no segmento de consórcios.

            A seguir está um conteúdo consolidado com as principais notícias econômicas da semana, separadas por temas. Sua tarefa é **formatar esse conteúdo como um relatório semanal profissional**, com linguagem analítica, clara e concisa.

            ---

            ## 📌 Instruções obrigatórias:

            - Adicione um **título institucional** ao relatório.

            - Em seguida, apresente o conteúdo detalhado das notícias, organizando em **microsessões** com **títulos curtos e descritivos**.
            - Cada título de seção deve ser **clicável**, contendo o **link da fonte mais relevante incorporado ao título** (em Markdown: `[Título](link)`).
            - Não repita o link no corpo do texto ou em seção separada.

            - Organize os tópicos por blocos temáticos, seguindo a ordem:
            1. **Macroeconomia e seu impacto no nosso mercado**
            2. **Mercado de Consórcios**
            3. **Banco Central**

            - O conteúdo deve ser **menos descritivo** e **mais analítico e objetivo**:
            - Evite repetir detalhes óbvios ou generalidades.
            - Vá direto ao ponto com foco em impactos e insights.
            - Sempre que possível, relacione com o setor de consórcios: poder de compra, custo do crédito, mercado consumidor, etc.

            - Siga os princípios da **brevidade inteligente**:
            - Clareza: linguagem direta, sem jargões desnecessários.
            - Objetividade: evite redundâncias e floreios.
            - Precisão: use os termos mais adequados para o contexto.
            - Impacto: destaque o que é crítico para a tomada de decisão.

            - Finalize com uma **Conclusão Executiva**, resumindo os principais alertas ou aprendizados da semana de forma estratégica.

            ---

            ## 📰 Conteúdo base para detalhamento:

            **1. Macroeconomia:**  
            {macro}

            **2. Mercado de Consórcios:**  
            {consorcios}

            **3. Banco Central:**  
            {bcb}
            """



    result = llm.invoke(prompt)

    state["final_editorial"] = result.content
    return state