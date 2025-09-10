from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper_macro, formatar_resultados_serper
from utils.llm_factory import get_llm
from datetime import datetime
from dotenv import load_dotenv
import os
from utils.scraper import normalizar_e_dedup_links, enriquecer_com_texto_links, _montar_corpus_para_llm, _extrair_primeiro_json_array


load_dotenv()

data_hoje = datetime.now().strftime('%d de %B de %Y') 

def search_macro(state):
    """Busca e gera relatório sobre a macroecônomia do país"""
    query = " economia inflação juros recessão últimas notícias Brasil"

    noticias = buscar_noticias_serper_macro(query)

    if not noticias:
        mensagem = "⚠️ Nenhuma notícia encontrada sobre macroeconomia."
        print(mensagem)
        state["macro_enriquecidos"] = []
        state["search_macro"] = mensagem
        return state
    
    # 2) Normalizar/deduplicar URLs
    noticias = normalizar_e_dedup_links(noticias)

    # 3) Scraping: baixar HTML → extrair TEXTO
    noticias = enriquecer_com_texto_links(noticias, min_chars=400)

    completos = [n for n in noticias if n.get("texto_completo")]
    parciais  = [n for n in noticias if not n.get("texto_completo")]

    # 4) Montar CORPUS com base no texto extraído (se não houver completos, use todos mesmo assim)
    base_para_llm = _montar_corpus_para_llm(completos, parciais, preview_full=1200, preview_snip=300)


    prompt = f"""

        <prompt>
  <role>
    Você é um analista macroeconômico.  
    Leia e avalie as notícias de MACROECONOMIA e responda **APENAS** com um **JSON válido (array)**, sem comentários.
  </role>

  <rules>
    <rule>Use SOMENTE as informações dos itens de entrada (`itens_json`). Não invente dados.</rule>
    <rule>Aceite `texto_completo=true` ou `snippet` quando necessário (se snippet, seja conservador ao interpretar).</rule>
    <rule>Fontes preferenciais: IBGE (IPCA/PIB/PNAD), Banco Central (Selic/Crédito), Ipea, B3, Valor, Estadão, G1, Exame, CNN Brasil, InfoMoney e congêneres confiáveis.</rule>
    <rule>Exclua publieditoriais e vídeos sem transcrição.</rule>
    <rule>Deduplicação por link/título.</rule>
    <rule>Inclua somente os itens que tenham relação com empresas de consórcios. Gere 1 objeto por item. Preserve a ordem de entrada.</rule>
  </rules>

  <analysis_instructions>
    <point>Foque em indicadores com potencial de afetar consórcios: Selic, IPCA, câmbio, PIB, emprego/renda/consumo, crédito/inadimplência, confiança, risco-país.</point>
    <point>Em “por_que_importa”, conecte o fato macro ao setor: demanda por cotas, custo de oportunidade (juros), inadimplência/PDD, captação/funding, ticket médio.</point>
    <point>Atribua relevância (0.0–1.0):  
      - 0.90–1.00: Copom/Selic; IPCA/IBGE; choques macro significativos.  
      - 0.70–0.85: PIB, emprego (CAGED/PNAD), crédito/BCB, confiança.  
      - 0.40–0.65: análises/projeções com impacto moderado.  
      - <;0.40: periférico.  
    </point>
  </analysis_instructions>

  <input>
    <hoje>{data_hoje}</hoje>
    <itens>{base_para_llm}</itens>
  </input>

  <output>
    <schema>
      [
        {{
          "titulo": "<título original>",
          "achados_principais": [
            "<linha 1 com números/datas/órgãos>",
            "<linha 2>",
            "<linha 3 (4ª/5ª se necessário)>"
          ],
          "por_que_importa": "<canal de transmissão macro → consórcios>",
          "fonte": "<nome da fonte>",
          "link": "<URL>",
          "data": "<DD-MM-AAAA ou vazio se indeterminável>",
          "relevancia": 0.0
        }}
      ]
    </schema>
    <fallback>Se nenhum item for válido, responda []</fallback>
  </output>
</prompt>


    """

    llm = get_llm("search")
    result = llm.invoke(prompt)

    raw = result.content
    parsed = _extrair_primeiro_json_array(raw)

    # Guarda no state tanto os dados brutos enriquecidos quanto o resumo
    total = len(noticias)
    num_completos = len(completos)

    state["macro_llm_raw"] = raw             # resposta crua da LLM (string)
    state["macro_llm_json"] = parsed         # lista parseada (ou [])
    state["macro_enriquecidos"] = noticias   # itens com texto/scrape
    state["search_macro"] = f"[macro] coletadas={total}, completas={num_completos}"
    #print(state["search_macro"])

    #print(json.dumps(parsed, ensure_ascii=False, indent=2))
    return state
























    resumo_links = formatar_resultados_serper(noticias)

    data_execucao = datetime.now().strftime("%d/%m/%Y")

    prompt = f"""
        Data de execução do relatório: {data_execucao}
        Você é um analista econômico responsável por elaborar relatórios informativos para a diretoria de uma empresa de consórcios.

        Com base nas notícias publicadas na última semana sobre **indicadores macroeconômicos no Brasil**, elabore um relatório profissional:

        {resumo_links}
        Dê foco especial a indicadores como inflação, PIB, taxa de juros, desemprego e câmbio, bem como decisões de política monetária, projeções econômicas e eventos que possam impactar o sistema financeiro e o setor de consórcios.

        **Requisitos obrigatórios**:
        - Cite **explicitamente a fonte confiável** da informação (ex: ABAC, Valor Econômico, G1, Estadão, Exame, etc).
        - Apresente os dados de forma clara, detalhada e com linguagem profissional.
        - Separe as notícias por tópicos ou subtítulos, se necessário.

        **Formato esperado por item**:
        - **Título**: Título da notícia  
        - **Conteúdo**: [conteúdo detalhado em linguagem formal e acessível]
        - **Fonte**: Nome da fonte  
        - **Link**: URL da notícia 
        - **Data**: Data da notícia 

        Evite opiniões pessoais, especulações ou informações desatualizadas.
"""
    
    llm = get_llm("search")
    result = llm.invoke(prompt)
    state["search_macro"] = result.content
    print(result.content)
    return state
