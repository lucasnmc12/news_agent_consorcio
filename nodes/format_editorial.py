from utils.llm_factory import get_llm

llm = get_llm("formating")

def format_editorial(state):
    print("Formatando o texto para editorial final...")

    merged = state.get('merged_content', '')
    macro = state.get('search_macro', '')
    consorcios = state.get('search_consorcios', '')
    bcb = state.get('search_bcb', '')

    prompt = f"""
                Você é um assistente editorial especializado em geração de relatórios analíticos a partir de notícias econômicas.

                A seguir está um conteúdo já consolidado e bem estruturado, chamado de **pré-relatório**. Seu papel é **refinar** esse conteúdo para transformá-lo no **relatório final** que se chama "Na Mira da Controladoria".

                ⚠️ Muito importante: **não reescreva tudo do zero**. Mantenha a maioria do conteúdo intacto, apenas fazendo *lapidações inteligentes*, conforme as diretrizes abaixo.

                ---

                ## 🎯 Objetivo do Relatório Final

                Apresentar o conteúdo do pré-relatório de forma clara, impactante e pronta para ser entregue a um público executivo interessado no setor de consórcios e macroeconomia.

                ---

                ## ✏️ O que você deve fazer com o conteúdo:

                1. **Lapidar o texto original (pré-relatório)** sem descaracterizar:
                - Corrija pequenos vícios de linguagem e torne a leitura mais fluida.
                - Faça ajustes de tom e clareza, mantendo o estilo direto e analítico.

                2. **Transforme cada título de tópico em um link clicável:**
                - Encontre a **fonte mais relevante** de cada notícia/tópico.
                - Formate o título como `[Título do tópico](link)` em Markdown.
                - ❗️Não repita o link no corpo nem em seção separada.

                3. **Conecte com o setor de consórcios sempre que possível:**
                - Comente sobre impacto no poder de compra, custo do crédito, confiança do consumidor, inflação, Selic, inadimplência, etc.

                4. **Se a notícia tiver mais de 15 dias**, insira uma observação indicando não ser uma notícia recente:
                - Use tom informativo e amigável:

                5. **Siga os princípios da brevidade inteligente:**
                - **Clareza:** linguagem direta, sem jargões desnecessários.
                - **Objetividade:** evite redundâncias e floreios.
                - **Precisão:** use os termos mais adequados ao contexto.
                - **Impacto:** destaque o que é mais relevante para tomada de decisão.

                6. **Não assine o relatório.** Nunca inclua rodapés com autor ou gerador de IA.

                ---

                ## 📝 Pré-relatório (base para o trabalho):

                {merged}

                ---

                Agora, com base no pré-relatório acima, gere o relatório final lapidado e formatado.
                """




    result = llm.invoke(prompt)

    state["final_editorial"] = result.content
    return state