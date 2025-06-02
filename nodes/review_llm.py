from llm_factory import get_llm


llm = get_llm("review")

def review_llm(state):
    print ("Aplicando a revisão automática baseada no feedback...")
    feedback = state.get("feedback", "Melhore a clareza e a coesão do texto.")

    prompt = f"""
    Você é um editor de texto. Aqui está um texto que precisa ser revisado:

    Texto:
    {state.get('merged_content', '')}

    Feedback para revisão:
    {feedback}

    Aplique as correções necessárias, melhore a clareza, ajuste eventuais erros 
    e torne o texto mais profissional.
    """
    resposta = llm.invoke(prompt)

    # Atualiza o estado com o texto revisado 
    state["merged_content"] = resposta
    return state