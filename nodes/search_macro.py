from llm_factory import get_llm
from datetime import datetime


llm = get_llm("search")

def search_macro(state):
    print("Buscando notícias macroeconômicas...")
    data_execucao = datetime.now().strftime("%d/%m/%Y")
    prompt = """
        Data de execução do relatório: {data_execucao}
        Você é um analista econômico responsável por elaborar relatórios informativos para a diretoria de uma empresa de consórcios.

        Busque e resuma detalhadamente **as notícias mais recentes (publicadas nos últimos 15 dias)** sobre **indicadores macroeconômicos no Brasil**.

        Dê foco especial a temas como **inflação, PIB, taxa de juros, desemprego, política monetária, câmbio** e outras variáveis que impactam o sistema financeiro e o mercado de consórcios.

        **Requisitos obrigatórios**:
        - Informe a **data de publicação** de cada notícia.
        - Cite **explicitamente a fonte confiável** da informação (ex: Valor Econômico, G1, Estadão, CNN, etc).
        - Inclua o **link direto para a notícia original** ao final do relatório, em uma seção chamada **"Fontes e Links"**.
        - Apresente os dados de forma clara, objetiva e com linguagem profissional.
        - Separe as notícias por tópicos ou subtítulos, se necessário.

        **Formato esperado por item**:
        - **Data**: DD/MM/AAAA  
        - **Fonte**: Nome da fonte  
        - **Resumo**: [conteúdo em linguagem formal e acessível]

        Evite opiniões pessoais, especulações ou informações desatualizadas.
        """
    result = llm.invoke(prompt)
    state["search_macro"] = result.content
    return state