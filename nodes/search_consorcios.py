# from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper_consorcio, formatar_resultados_serper
from utils.llm_factory import get_llm
from datetime import datetime
import json
from dotenv import load_dotenv
from utils.scraper import normalizar_e_dedup_links, enriquecer_com_texto_links, _montar_corpus_para_llm, _extrair_primeiro_json_array

load_dotenv()

data_hoje = datetime.now().strftime('%d de %B de %Y') 

def search_consorcios(state):
    """Busca e gera relatório sobre o mercado de consórcios"""
    query = "mercado de consorcios"

    noticias = buscar_noticias_serper_consorcio(query)

    if not noticias:
        mensagem = "⚠️ Nenhuma notícia encontrada sobre consórcios."
        print(mensagem)
        state["consorcios_enriquecidos"] = []
        state["search_consorcios"] = mensagem
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
    Você é um analista especializado no setor de CONSÓRCIOS.  
    Leia e avalie as notícias fornecidas e responda **APENAS** com um **JSON válido (array)**, sem comentários.
  </role>

  <rules>
    <rule>Use SOMENTE as informações dos itens de entrada (`itens_json`). Não invente dados.</rule>
    <rule>Aceite itens com `texto_completo=true` ou apenas com `snippet` (quando o texto completo não estiver disponível). Se for snippet, seja conservador.</rule>
    <rule>Fontes confiáveis (preferência): ABAC, Valor Econômico, G1, Estadão, O Globo, Folha, Exame, CNN Brasil, InfoMoney, bcb.gov.br e órgãos oficiais.</rule>
    <rule>Exclua publieditoriais e vídeos sem transcrição (ex.: “especial-publicitário”, “publieditorial”, páginas de vídeo).</rule>
    <rule>Deduplicação: se dois itens forem o mesmo fato (mesmo link ou título muito semelhante), mantenha apenas um (o mais completo/mais claro).</rule>
    <rule>Inclua TODOS os itens válidos. Gere 1 objeto por item que passar nos filtros. Preserve a ordem de entrada.</rule>
  </rules>

  <analysis_instructions>
    <point>Leia o campo `texto` quando existir; caso contrário, use `snippet`. Não extrapole números não presentes no conteúdo.</point>
    <point>Em “por_que_importa”, conecte explicitamente ao setor de consórcios: adesões, créditos comercializados, ticket médio, contemplações/lances, captação, inadimplência/PDD, fraudes, operações (M&amp;A), parcerias, tecnologia/produto, mudanças regulatórias.</point>
    <point>Atribua relevancia ∈ [0.0, 1.0]:  
      - 0.90–1.00: dados oficiais ABAC/setoriais; decisões regulatórias que afetam diretamente consórcios; choques relevantes.  
      - 0.70–0.85: movimentações de empresas com impacto setorial; fraudes relevantes; M&amp;As; indicadores operacionais do setor.  
      - 0.40–0.65: notícias corporativas com efeito indireto/moderado.  
      - &lt;0.40: periférico (considere descartar se pouco informativo).  
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
            "<linha 1 baseada em fato verificável>",
            "<linha 2>",
            "<linha 3 (pode haver 4ª/5ª linha se for muito relevante)>"
          ],
          "por_que_importa": "<conexão explícita com o setor de consórcios>",
          "fonte": "<nome da fonte>",
          "link": "<URL>",
          "data": "<DD-MM-AAAA ou vazio se indeterminável>",
          "relevancia": 0.0
        }}
      ]
    </schema>
    <fallback>Se nenhum item for válido após os filtros, responda []</fallback>
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

    state["consorcios_llm_raw"] = raw             # resposta crua da LLM (string)
    state["consorcios_llm_json"] = parsed         # lista parseada (ou [])
    state["consorcios_enriquecidos"] = noticias   # itens com texto/scrape
    state["search_consorcios"] = f"[consórcios] coletadas={total}, completas={num_completos}"
    #print(state["search_consorcios"])

    #print(json.dumps(parsed, ensure_ascii=False, indent=2))
    return state
    
    









