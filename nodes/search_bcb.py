from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper, buscar_noticias_serper_bacen
from searcher_gemini import buscar_noticias_gemini
from searcher_gemini import buscar_noticias_gemini
from utils.llm_factory import get_llm
from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv
import os
from utils.scraper import normalizar_e_dedup_links, enriquecer_com_texto_links, _montar_corpus_para_llm, _extrair_primeiro_json_array


load_dotenv() 

data_hoje = datetime.now().strftime('%d de %B de %Y') 

def search_bcb(state):
    """Busca e gera relatório sobre Banco Central"""
    query = """Banco Central do Brasil últimas notícias"""

    noticias = buscar_noticias_serper_bacen(query)

    if not noticias:
        mensagem = ("⚠️ Nenhuma notícia encontrada.")
        print(mensagem)
        state["bcb_enriquecidos"] = []
        state["search_bcb"] = mensagem
        return state
    
    # 2) Normalizar/deduplicar URLs
    noticias = normalizar_e_dedup_links(noticias)

    # 3) Scraping: baixar HTML → extrair TEXTO
    noticias = enriquecer_com_texto_links(noticias, min_chars=400)

    completos = [n for n in noticias if n.get("texto_completo")]
    parciais  = [n for n in noticias if not n.get("texto_completo")]

# 4) Montar CORPUS com base no texto extraído (se não houver completos, use todos mesmo assim)
    base_para_llm = _montar_corpus_para_llm(completos, parciais, preview_full=1200, preview_snip=300)

    prompt = f""""

    Você é um analista regulatório. Leia e avalie as notícias relacionadas ao BANCO CENTRAL/CMN/Copom e responda **APENAS** com um **JSON válido (array)**, sem comentários.

    REGRAS (obrigatórias):
    - Use SOMENTE as informações dos itens de entrada (`itens_json`). Não invente dados.
    - Aceite `texto_completo=true` ou apenas `snippet` (se não houver texto completo). Se for snippet, seja conservador.
    - Priorize atos/temas: Resoluções/Resoluções CMN, Circulares, Comunicados, Consultas Públicas, Copom/Selic, Pix/Open Finance, registradoras, SCR, compliance/supervisão.
    - Fontes preferenciais: bcb.gov.br, CMN, e cobertura de imprensa econômica confiável (Valor, Estadão, G1, Exame, InfoMoney etc.).
    - Exclua publieditoriais e vídeos sem transcrição.
    - Deduplicação: se forem o mesmo fato (mesmo link/título), mantenha o mais completo.
    - **Inclua TODOS os itens válidos**. Gere **1 objeto por item**. Preserve a ordem de entrada.

    INSTRUÇÕES DE ANÁLISE:
    - Reflita com precisão o teor regulatório e a decisão/consulta/comunicado.
    - Em “por_que_importa”, explique o efeito sobre administradoras de consórcios: exigências regulatórias, reporte, provisões/risco, capital/funding, liquidez, processos de compliance/auditoria, impacto operacional (Pix/Open Finance/infra).
    - Relevância (0.0–1.0):
      - 0.95–1.00: normas oficiais (Resolução/Circular/Lei) com impacto direto; decisões Copom/Selic.
      - 0.80–0.90: comunicados/ofícios/consultas com alta probabilidade de impacto.
      - 0.60–0.75: falas/sinalizações relevantes; enforcement setorial.
      - <0.60: menções periféricas/baixa materialidade.

    ENTRADA:
    - Hoje: {data_hoje}
    - Itens (JSON):
    {base_para_llm}

    SAÍDA (JSON array). Schema por elemento:

    [
      {{
        "titulo": "<título original>",
        "achados_principais": [
          "<linha 1 com o que foi decidido/consultado/ comunicado>",
          "<linha 2 com números/datas/alcance quando existirem>",
          "<linha 3 (4ª/5ª se necessário, mantendo factual)>"
        ],
        "por_que_importa": "<efeito prático para administradoras de consórcios>",
        "fonte": "<nome da fonte>",
        "link": "<URL>",
        "data": "<DD-MM-AAAA ou vazio se indeterminável>",
        "relevancia": 0.0
      }}
    ]

    Se nenhum item for válido, responda **[]**.

                    
    """


    llm = get_llm("search")
    result = llm.invoke(prompt)

    raw = result.content
    parsed = _extrair_primeiro_json_array(raw)

    # Guarda no state tanto os dados brutos enriquecidos quanto o resumo
    total = len(noticias)
    num_completos = len(completos)


    state["bcb_llm_raw"] = raw             # resposta crua da LLM (string)
    state["bcb_llm_json"] = parsed         # lista parseada (ou [])
    state["bcb_enriquecidos"] = noticias   # itens com texto/scrape
    state["search_bcb"] = f"[Banco Central] coletadas={total}, completas={num_completos}"
    #print(state["search_bcb"])

    #print(json.dumps(parsed, ensure_ascii=False, indent=2))
    return state