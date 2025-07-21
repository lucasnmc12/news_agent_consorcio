from utils.llm_factory import get_llm
 
llm = get_llm("merge")

def merged_content(state):
    prompt = f"""
        Você é um editor sênior responsável por preparar um **pré-relatório executivo semanal** para a controladoria de uma empresa do setor de consórcios.

        Sua tarefa é **selecionar, organizar e consolidar as informações mais relevantes** a partir dos três blocos temáticos abaixo, unindo os dados em um único texto separado em 3 blocos: Macoreconomia, Mercado de consórcios e Banco Central, bem estruturado e pronto para ser formatado em um relatório editorial posterior.

        - Banco Central: {state.get('search_bcb', '')}
        - Consórcios: {state.get('search_consorcios', '')}
        - Macroeconomia: {state.get('search_macro', '')}

        **Critérios de relevância**:
        - Dê prioridade a **indicadores macroeconômicos** (inflação, PIB, taxa de juros,desemprego, câmbio);
        - Destaque **decisões e comunicados oficiais do Banco Central**, especialmente sobre taxa Selic e política monetária;
        - Selecione **notícias do setor de consórcios** que tratem de crescimento, comportamento do consumidor, mudanças regulatórias, fusões, fraudes e novas tecnologias com impacto direto no mercado.
        - Dê preferência às notícias provenientes de fontes confiáveis, como: Valor Econômico, G1, Estadão, Exame, CNN Brasil, InfoMoney, Reuters, ABAC, Banco Central, entre outras.
        - Priorize esses conteúdos na seleção e organização dos dados.
        - Se houver conflitos de informação ou duplicidade, mantenha a versão publicada por uma fonte da lista acima.

        **Critérios obrigatórios**:
        - Destaque apenas os trechos com informações mais relevantes e recentes.
        - Remova repetições, dados pouco úteis ou redundantes.
        - Mantenha a **data de publicação** e a **fonte** visível em cada item.
        - Não formate como relatório final — esta é uma etapa de **pré-processamento editorial**.
        - Ao final, adicione uma seção "Fontes e Links" com os links numerados ([1], [2], [3]...).
        

        Este documento será usado como base para o relatório final. Sua função é **organizar e filtrar as informações**, não gerar o conteúdo definitivo de apresentação.
        """


    result = llm.invoke(prompt)
    state ['merged_content'] = result.content
    return state