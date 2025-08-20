from utils.llm_factory import get_llm
from datetime import datetime, date

llm = get_llm("formating")

data_hoje = datetime.now().strftime('%d de %B de %Y') 

def format_editorial(state):
    print("Formatando o texto para editorial final...")

    merged = state.get('merged_content', '')
    macro = state.get('search_macro', '')
    consorcios = state.get('search_consorcios', '')
    bcb = state.get('search_bcb', '')

    prompt = f"""
                Você é um editor profissional. Formate o conteúdo APROVADO abaixo em um RELATÓRIO FINAL para o gerente de uma administradora de consórcios.

        REGRAS DE FIDELIDADE (OBRIGATÓRIAS):
        - NÃO adicione, omita ou altere informações. NÃO inclua novas fontes ou números.
        - Mantenha todos os itens aprovados, apenas melhorando clareza, ortografia e padronização.
        - Preserve a ordem por TEMA (BCB, Macroeconomia, Consórcios). Dentro de cada tema, use a ordem que vier no conteúdo aprovado.
        - Se algum item não tiver data, deixe em branco (não invente). Se não houver link, não crie link.

        REGRAS DE FORMATAÇÃO:
        - Saída em **Markdown**.
        - Título de cada notícia deve ser **clicável**: `### [<título>](<link>) — *<fonte>*, <data>`
        - Logo abaixo do título, use subblocos padronizados:
        - **Essência (fatos verificados):**
            - Converta `achados_principais` em 2–5 bullets, sem reescrever números.
        - **Por que importa (setor de consórcios):**
            - Traga o texto aprovado em 1–2 linhas (sem extrapolar).
        - **Relevância:** `<valor de 0.00 a 1.00>`

        - Padronizações:
        - Datas no formato DD-MM-AAAA quando disponíveis no conteúdo aprovado.
        - Números, percentuais e órgãos devem aparecer como no aprovado (sem arredondar ou reinterpretar).
        - Links sempre entre `()` no título.

        ESTRUTURA DO RELATÓRIO:

        # Relatório Final — Inteligência de Mercado (Consórcios)
        **Empresa:** Multimarcas Consórcios 
        **Data:** {data_hoje}

        ## Sumário Executivo
        - Em 4–6 linhas, descreva APENAS com base no conteúdo aprovado os principais riscos, oportunidades e pontos de atenção para a gestão. Não inclua nada que não esteja explícito nos itens.

        ## Banco Central (BCB)
        > Decisões/atos/comunicados com efeito regulatório ou operacional para administradoras de consórcios.

        <!-- Liste todas as notícias deste tema -->
        ### [<título>](<link>) — *<fonte>*, <data>
        **Essência (fatos verificados):**
        - ...
        **Por que importa (setor de consórcios):** ...
        **Relevância:** 0.00

        <!-- Repita o bloco para cada item de BCB aprovado -->

        ## Macroeconomia
        > Indicadores/choques com efeito em demanda, risco, funding e preço.

        ### [<título>](<link>) — *<fonte>*, <data>
        **Essência (fatos verificados):**
        - ...
        **Por que importa (setor de consórcios):** ...
        **Relevância:** 0.00

        <!-- Repita para todos os itens de Macroeconomia aprovados -->

        ## Consórcios (Setor/Empresas)
        > Movimentos setoriais, dados ABAC, empresas, fraudes, parcerias/M&A.

        ### [<título>](<link>) — *<fonte>*, <data>
        **Essência (fatos verificados):**
        - ...
        **Por que importa (setor de consórcios):** ...
        **Relevância:** 0.00

        <!-- Repita para todos os itens de Consórcios aprovados -->

        ## Anexos — Fontes Utilizadas
        - Liste todas as notícias (por tema): <fonte> — <título> (<data>) — <link>

        CONTEÚDO APROVADO (não modifique fatos, apenas formate):

        {state.get('merged_content')}

                """




    result = llm.invoke(prompt)

    state["final_editorial"] = result.content
    return state