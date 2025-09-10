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
        <prompt>
  <role>
    Você é um editor profissional.  
    Formate o conteúdo APROVADO abaixo em um RELATÓRIO FINAL para o gerente de uma administradora de consórcios.
  </role>

  <rules_fidelity>
    <rule>NÃO adicione, omita ou altere informações. NÃO inclua novas fontes ou números.</rule>
    <rule>Mantenha todos os itens aprovados, apenas melhorando clareza, ortografia e padronização.</rule>
    <rule>Preserve a ordem por TEMA (BCB, Consórcios, Macroeconomia). Dentro de cada tema, use a ordem que vier no conteúdo aprovado.</rule>
    <rule>Se algum item não tiver data, deixe em branco (não invente). Se não houver link, não crie link.</rule>
    <rule>Se algum item tiver mais de 28 dias, descarte o item do resultado gerado. {data_hoje}</rule>
    <rule>Ordene os itens por data, o mais recente primeiro. Não descarte a agrupação por tema.</rule>
    <rule>Mantenha no máximo 4 itens por tema, descarte o menos relevante.</rule>
  </rules_fidelity>

  <rules_formatting>
    <rule>Saída em Markdown.</rule>
    <rule>Título de cada notícia deve ser clicável: `### [<título>](<link>) — *<fonte>*`</rule>
    <rule>Logo abaixo do título, use subblocos padronizados: bullets de 2–5 linhas a partir de `achados_principais`.</rule>
    <rule>Quebra de linha entre cada subbloco.</rule>
    <rule><strong>Por que importa:</strong> → reescreva o texto aprovado em forma nominalizada, até 4 linhas.</rule>
    <rule><strong>Ações futuras:</strong> → crie seção final com recomendações, separando:  
      - "Movimentos recomendados pra ontem" (próximas 48h).  
      - "Ficar de olho" (próximos 7 dias).  
    </rule>
    <rule>Datas no formato DD/MM/AAAA.</rule>
    <rule>Números, percentuais e órgãos devem aparecer como no aprovado (sem arredondar).</rule>
    <rule>Links sempre entre parênteses no título.</rule>
  </rules_formatting>

  <structure>
    # Na Mira da Controladoria - Relatório Quinzenal  
    **Data:** {data_hoje} em português

    ## Sumário Executivo  
    - De 3–6 bullets, descrevendo APENAS com base no conteúdo aprovado os principais riscos, oportunidades e pontos de atenção.

    ## Banco Central (BCB)  
    ### [<título>](<link>) — *<fonte>*  
    - <bullet 1 de achados_principais>  
    - <bullet 2>  
    - Quebra de linha
    **Por que importa:** <texto reescrito>  
    - Quebra de linha
    **Data:** DD/MM/AAAA  

    ## Mercado de Consórcios  
    ### [<título>](<link>) — *<fonte>*  
    - <bullet 1 de achados_principais>  
    - <bullet 2>  
    - Quebra de linha
    **Por que importa:** <texto reescrito>  
    - Quebra de linha
    **Data:** DD/MM/AAAA  

    ## Economia  
    ### [<título>](<link>) — *<fonte>*  
    - <bullet 1 de achados_principais>  
    - <bullet 2>  
    - Quebra de linha
    **Por que importa:** <texto reescrito>  
    - Quebra de linha
    **Data:** DD/MM/AAAA  

    ## Ações futuras:  
    ### Movimentos recomendados "pra ontem"  
    - <bullet 1>  
    - <bullet 2>  
    ### Ficar de olho  
    - <bullet 1>  
    - <bullet 2>  

    ### Anexos — Fontes Utilizadas  
    - Os links estão inseridos nos respectivos títulos.
  </structure>

  <input>
    <conteudo_aprovado>{state.get('merged_content')}</conteudo_aprovado>
  </input>
</prompt>
                """




    result = llm.invoke(prompt)

    state["final_editorial"] = result.content
    return state