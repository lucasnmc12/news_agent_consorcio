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
        - Preserve a ordem por TEMA (BCB, Consórcios, Macroeconomia). Dentro de cada tema, use a ordem que vier no conteúdo aprovado.
        - Se algum item não tiver data, deixe em branco (não invente). Se não houver link, não crie link.
        - Se algum item tiver mais de 28 dias, descarte o item do resultado gerado. {data_hoje}
        - Ordene os itens por relevância, o mais relevante primeiro. Não descarte a agrupação por tema.

        REGRAS DE FORMATAÇÃO:
        - Saída em **Markdown**.
        - Título de cada notícia deve ser **clicável**: `### [<título>](<link>) — *<fonte>*
        - Logo abaixo do título, use subblocos padronizados:
            - Converta de forma mais direta os `achados_principais` em 2–5 bullets, com quebras de linhas se for possível sem comprometer o sentido, sem reescrever números.
        - Quebra de linha
        - **Por que importa: **
            - Reescreva o texto aprovado, que está no infinitivo impessoal, em uma forma nominalizada, destacando a importância da ação. Até 4 linhas (sem extrapolar).
        - Quebra de linha
        - **Relevância:** `<valor de 0.00 a 1.00>`
        - **Ações futuras:**
            - A última seção do relatório deve conter recomendações de ações futuras com base no conteúdo aprovado.
            - Os itens da seção # Ações Recomendadas (próximas 48h) estarão no sub-bloco "Movimentos recomendados "pra ontem"
            - Os itens da seção ## Itens para Monitorar (próximos 7 dias) estarão no sub-bloco "Ficar de olho"    

        - Padronizações:
        - Datas no formato DD-MM-AAAA quando disponíveis no conteúdo aprovado.
        - Números, percentuais e órgãos devem aparecer como no aprovado (sem arredondar ou reinterpretar).
        - Links sempre entre `()` no título.
        - Quebra de linha a cada sub-tópico

        ESTRUTURA DO RELATÓRIO:

        # Na Mira da Controladoria - Relatório Quinzenal 
        **Data:** ...

        ## Sumário Executivo
        - Em 3–6 linhas, separando cada assunto por tópicos, descreva APENAS com base no conteúdo aprovado os principais riscos, oportunidades e pontos de atenção para a gestão. Não inclua nada que não esteja explícito nos itens.

        ## Banco Central (BCB)
        > Decisões/atos/comunicados com efeito regulatório ou operacional das últimas semanas.

        <!-- Liste todas as notícias deste tema -->
        ### [<título>](<link>) — *<fonte>*
        **(Os tópicos mais relevantes nessa seção, sem título antes) **
        - ...
        - Quebra de linha
        **Por que importa:** ...
        - Quebra de linha
        **Data:** DD/MM/AAAA
        - Quebra de linha
        **Relevância:** 0.00

        <!-- Repita o bloco para cada item de BCB aprovado -->

        ## Mercado de Consórcios
        > Movimentos setoriais, dados ABAC, empresas, fraudes, parcerias/M&A.

        ### [<título>](<link>) — *<fonte>*
        - ...
        - Quebra de linha
        **Por que importa:** ...
        - Quebra de linha
        **Data:** DD/MM/AAAA
        - Quebra de linha
        **Relevância:** 0.00

        <!-- Repita para todos os itens de Consórcios aprovados -->

        ## Economia
        > Indicadores/choques com efeito em demanda, risco, funding e preço.

        ### [<título>](<link>) — *<fonte>*
        - ...
        - Quebra de linha
        **Por que importa:** ...
        - Quebra de linha
        **Data:** DD/MM/AAAA
        - Quebra de linha
        **Relevância:** 0.00

        <!-- Repita para todos os itens de Macroeconomia aprovados -->

        - ## Ações futuras:
            - Quebra de linha 
            - A última seção do relatório deve conter recomendações de ações futuras com base no conteúdo aprovado.
            - Os itens da seção # Ações Recomendadas (próximas 48h) estarão no sub-bloco ### Movimentos recomendados "pra ontem"
            - Quebra de linha a cada item
            - Os itens da seção ## Itens para Monitorar (próximos 7 dias) estarão no sub-bloco ### Ficar de olho
            - Quebra de linha a cada item


        ### Anexos — Fontes Utilizadas
        - Os links utilizados para a pesquisa e coleta de informações estão inseridos nos respectivos títulos.

        CONTEÚDO APROVADO (não modifique fatos, apenas formate):

        {state.get('merged_content')}

                """




    result = llm.invoke(prompt)

    state["final_editorial"] = result.content
    return state