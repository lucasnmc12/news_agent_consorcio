from llm_factory import get_llm


llm = get_llm("review")

def review_llm(state):
    print ("Aplicando a revisão automática baseada no feedback...")
    feedback = state.get("feedback", "Melhore a clareza e a coesão do texto.")

    prompt = f"""
        Você é um editor profissional encarregado de revisar um relatório econômico que será entregue à diretoria de uma empresa de consórcios.

        Aqui está o conteúdo a ser revisado:
        {state.get('merged_content', '')}

        Comentários ou instruções específicas de revisão:
        {feedback}

        **Sua tarefa**:
        - Aplique melhorias com base no feedback fornecido.
        - Corrija erros gramaticais e de digitação, se houver.
        - Aumente a clareza, coesão e profissionalismo do texto.
        - Mantenha a estrutura editorial, datas, fontes e links presentes no conteúdo.

        Retorne o texto final já revisado.
        """
    resposta = llm.invoke(prompt)

    # Atualiza o estado com o texto revisado 
    state["merged_content"] = resposta.content
    return state