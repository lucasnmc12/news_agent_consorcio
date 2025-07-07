from utils.llm_factory import get_llm

llm = get_llm("formating")

def format_editorial(state):
    print("Formatando o texto para editorial final...")

    merged = state.get('merged_content', '')
    macro = state.get('search_macro', '')
    consorcios = state.get('search_consorcios', '')
    bcb = state.get('search_bcb', '')

    prompt = f"""
        Você é um editor sênior responsável por preparar **relatórios informativos semanais**, voltados ao setor da Controadoria da empresa "Multimarcas Consórcios" do setor de consórcios.

        A seguir está um conteúdo consolidado com as principais notícias econômicas da semana, separadas por temas. Sua tarefa é **formatar esse conteúdo como um relatório semanal profissional**, com clareza, estrutura lógica e linguagem analítica.

        ---

        ## 📌 Instruções obrigatórias:

        - Adicione um **título institucional** ao relatório.
        - Inclua uma **introdução breve**, explicando o objetivo do relatório e o período analisado.
        - Após a introdução, insira um **resumo geral do conteúdo** com base no fornecido abaixo.

        ### 🔹 Resumo Base:
        {merged}

        - Em seguida, apresente o conteúdo detalhado das notícias, organizando em **microsessões** com **títulos descritivos e curtos** (ex.: "Alta da Selic", "Dólar em Alta", "Consórcios em Crescimento").
        - Organize os tópicos por blocos temáticos, seguindo a ordem:
        1. **Macroeconomia**
        2. **Mercado de Consórcios**
        3. **Banco Central**

        - IMPORTANTE: Sempre que possível, **relacione os eventos macroeconômicos com o impacto potencial ou real no mercado de consórcios**, como efeitos sobre o poder de compra dos consumidores, custo do crédito, confiança do mercado, entre outros.

        - IMPORTANTE: 
        - O texto deve seguir os **princípios de brevidade inteligente**:
        - Clareza: linguagem simples e direta.
        - Objetividade: sem redundâncias ou floreios.
        - Precisão: palavras exatas, com foco no essencial.
        - Impacto: destaque os pontos críticos e relevantes para a tomada de decisão.
        

        - Finalize com uma **conclusão executiva**, destacando os principais aprendizados ou sinais de alerta da semana.

        ---

        ## 🔗 Sobre os links:

        - **Não inclua links no corpo do texto.**
        - Ao final do relatório, adicione uma seção chamada **"Fontes e Links"**.
        - Liste os links utilizados em ordem numérica ([1], [2], [3]...)
        - IMPORTANTE: * Cada link deve estar em uma linha separada, com quebra de linha visível.* ATENÇÃO

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