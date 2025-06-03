from llm_factory import get_llm

llm = get_llm("formating")

def format_editorial(state):
    print("Formatando o texto para editorial final...")
    prompt = f"""
        Você é um editor sênior responsável por preparar relatórios informativos para a diretoria de uma empresa de consórcios.

        A seguir está o conteúdo consolidado das principais notícias econômicas da semana. Formate esse conteúdo como um **relatório semanal profissional**, pronto para ser apresentado à diretoria.

        **Instruções obrigatórias**:
        - Adicione um **título institucional** ao relatório.
        - Inclua uma **introdução breve**, apresentando o objetivo do relatório.
        - Estruture o texto em **seções com subtítulos claros** (ex: Banco Central, Macroeconomia, Consórcios).
        - Mantenha o conteúdo claro, objetivo e com linguagem profissional.
        - Finalize com uma **conclusão executiva** resumindo os principais pontos.
        - Ao final do documento, adicione uma seção chamada **"Fontes e Links"**, contendo os links originais de cada notícia, se disponíveis.

        Conteúdo a ser formatado:
        {state.get('merged_content', '')}
        """
    result = llm.invoke(prompt)

    state["final_editorial"] = result.content
    return state