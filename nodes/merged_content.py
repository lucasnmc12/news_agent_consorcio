from utils.llm_factory import get_llm
from datetime import datetime, date
 
llm = get_llm("merge")

data_hoje = datetime.now().strftime('%d de %B de %Y') 

def merged_content(state):
    prompt = f"""

    Você é um analista sênior. Converta as notícias abaixo em um PRÉ-RELATÓRIO objetivo para o gerente de uma administradora de consórcios.

            AUDIÊNCIA:
            - Gerente de consórcios (foco prático): volume de adesões/créditos, ticket médio, contemplações/lances, inadimplência/PDD, cancelamentos, fraudes, reputação, funding/custo financeiro, mudanças regulatórias e impactos operacionais.

            REGRAS GERAIS (obrigatórias):
            - Use SOMENTE o conteúdo fornecido nos itens. NÃO invente dados nem traga fontes externas.
            - Se a data da notícia tiver mais de 28 dias, descarte o item do resultado gerado.
            - Os itens vêm em um array JSON, cada um com: titulo, achados_principais[], por_que_importa, fonte, link, data (DD-MM-AAAA ou vazio), relevancia (0.0–1.0) e origem ∈ (bcb, macro, consorcios).
            - Agrupe a saída por TEMA: Banco Central (BCB), Macroeconomia, Consórcios (setor/empresas).
            - Dentro de cada tema, **ordene por relevancia desc**. Se houver muitos itens, priorize os mais relevantes e consolide duplicatas (mesmo fato) em um único bloco.
            - Preserve números, datas e órgãos exatamente como informados. Se “data” estiver vazia, não invente.
            - Seja conciso, profissional, sem adjetivos desnecessários.

            ENTRADA:
            - Data de referência: {data_hoje}
            - Itens (JSON):
            {state.get('news_unificadas_json')}

            FORMATO DE SAÍDA (Markdown):

            # Pré-Relatório — Consórcios
            **Data:** {data_hoje}

            ## Sumário Executivo (2–5 linhas)
            - Principais fatos do período (o que muda decisão)
            - Riscos e oportunidades mais relevantes para operação, P&L e caixa
            - Pointers para ações imediatas (quando existirem)

            ## Banco Central (BCB)
            > Decisões/atos/comunicados que afetam diretamente administradoras de consórcios.

            Para cada notícia:
            **Título:** <título> — *<fonte>*, <data>  
            **Essência (fatos verificados):**
            - <2–3 bullets a partir de "achados_principais">
            **Impacto para a operação/risco:**
            - <1–2 bullets traduzindo por_que_importa para ação gerencial (ex.: compliance, reporte, funding, processo)>
            **Link:** <URL>  | **Relevância:** <0.00–1.00>

            Se não houver itens aqui: *Sem novidades relevantes neste tema.*

            ## Macroeconomia
            > Indicadores/choques com efeito sobre demanda, risco e custo financeiro.

            Para cada notícia :
            **Título:** <título> — *<fonte>*, <data>  
            **Essência (fatos verificados):**
            - <2–3 bullets a partir de "achados_principais">
            **Transmissão para consórcios:**
            - <1–2 bullets a partir de "por_que_importa" (ex.: demanda, ticket, inadimplência, captação)>
            **Link:** <URL>  | **Relevância:** <0.00–1.00>

            Se não houver itens aqui: *Sem novidades relevantes neste tema.*

            ## Consórcios (setor/empresas)
            > Movimentos do setor, empresas, fraudes, reputação, dados ABAC.

            Para cada notícia :
            **Título:** <título> — *<fonte>*, <data>  
            **Essência (fatos verificados):**
            - <2–3 bullets a partir de "achados_principais">
            **Implicações gerenciais:**
            - <1–2 bullets práticos para operação/comercial/risco>
            **Link:** <URL>  | **Relevância:** <0.00–1.00>

            Se não houver itens aqui: *Sem novidades relevantes neste tema.*

            ## Ações Recomendadas (próximas 48h)
            - <bullet 1 objetivo e atribuível>
            - <bullet 2>
            - <bullet 3>

            ## Itens para Monitorar (próximos 7 dias)
            - <bullet 1 — dado esperado, decisão regulatória, release ABAC/IBGE/BCB>
            - <bullet 2>
            - <bullet 3>

            ## Apêndice — Fontes
            - Liste por tema: <fonte> — <título> (<data>) — <link>

            INSTRUÇÕES FINAIS:
            - Não repita o mesmo fato em mais de um tema; mantenha onde o impacto for mais direto.
            - Se “por_que_importa” vier genérico, traduza para implicação concreta de gestão (ex.: revisar premissas de PDD, ajustar metas de captação, reforçar compliance).
            - Saída: **apenas o relatório em Markdown**, sem texto extra fora da estrutura.

    
        """


    result = llm.invoke(prompt)
    state ['merged_content'] = result.content
    return state