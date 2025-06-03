from llm_factory import get_llm

llm = get_llm("formating")

def format_editorial(state):
    print("Formatando o texto para editorial final...")
    prompt = f"""
    Você é um editor de publicações. Formate o seguinte texto como um relatório semanal. 
    Inclua título, subtítulos, seções bem definidas, uma introdução e uma conclusão. 
    Mantenha clareza, objetividade e profissionalismo.

    Texto:
    {state.get('merged_content', '')}
    """
    result = llm.invoke(prompt)

    state["final_editorial"] = result.content
    return state