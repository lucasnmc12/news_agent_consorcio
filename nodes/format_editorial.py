from utils.llm_factory import get_llm

llm = get_llm("formating")

def format_editorial(state):
    print("Formatando o texto para editorial final...")
    prompt = f"""
        Você é um editor sênior responsável por preparar relatórios informativos para a diretoria de uma empresa de consórcios.

        A seguir está o conteúdo consolidado das principais notícias econômicas da semana. Formate esse conteúdo como um **relatório semanal profissional**, pronto para ser apresentado à diretoria.

        **Instruções obrigatórias**:
        - Adicione um **título institucional** ao relatório.
        - Inclua uma **introdução breve**, apresentando o objetivo do relatório.
        - Estruture o texto em **microsessões**, com **títulos descritivos e curtos** (ex: "Selic Mantida em 10,5%", "Alta na Inflação de Alimentos", etc.).
        - Organize os temas em blocos lógicos como **Banco Central**, **Macroeconomia** e **Consórcios**.
        - Mantenha o conteúdo claro, objetivo, detalhado e com linguagem profissional e analítica.
        - Finalize com uma **conclusão executiva**, resumindo os principais pontos relevantes da semana.

        **Sobre os links**:
        - Não inclua links no corpo do texto.
        - Ao final do relatório, crie uma seção chamada **"Fontes e Links"**.
        - Liste os links utilizados em ordem numérica ([1], [2], [3]...) com o título da notícia ou tema correspondente, com quebra de linha e link clicável em cada um deles.
        - Sempre que possível, associe os dados apresentados aos respectivos links.

        Conteúdo a ser formatado:
        {state.get('merged_content', '')}
        """

    result = llm.invoke(prompt)

    state["final_editorial"] = result.content
    return state