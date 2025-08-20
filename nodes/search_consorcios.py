# from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper
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

    noticias = buscar_noticias_serper(query)

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
        Você é um analista econômico objetivo. Leia e avalie notícias completas sobre o mercado de consórcios no Brasil. Responda **APENAS** com JSON válido (um array), sem comentários adicionais.

        REGRAS DE FILTRO (obrigatórias):
        1) Considere **somente** matérias publicadas nos **últimos 16 dias** em relação a {data_hoje}.
        - O campo de data pode vir como ISO (ex.: 2025-08-10) ou relativo (ex.: "há 3 dias"). Converta para **DD-MM-AAAA**.
        2) **Fontes confiáveis apenas**: priorize domínios como ABAC, Valor Econômico, G1, Estadão, O Globo, Folha, Exame, CNN Brasil, InfoMoney, bcb.gov.br, IBGE, Ipea, B3. 
        3) **Deduplicação**: se vários itens tratarem do mesmo fato, mantenha o mais completo/mais claro (ou o da fonte original) e descarte o resto.

        INSTRUÇÕES DE ANÁLISE:
        - Leia o **campo `texto`** integralmente; não invente dados que não estejam nele.
        - Seja 100% factual: números, percentuais, datas, órgãos e nomes **precisam** estar no texto.
        - Escreva "Achados principais" em **3 a 5 linhas** (bullets implícitos em frases separadas).
        - Em "Por que importa", conecte o fato **explicitamente** ao setor de consórcios (demanda, ticket, inadimplência, captação, regulação, operações, etc.).
        - Atribua "Relevancia" entre **0.0 e 1.0**:
        - 0.9–1.0: decisões regulatórias (BCB/CMN/Copom), mudanças na Selic, dados setoriais oficiais (ABAC), choques macro relevantes.
        - 0.7–0.8: indicadores macro com impacto claro no setor, grandes operações/fraudes, M&As relevantes.
        - 0.4–0.6: notícias de empresas com algum efeito no setor.
        - <0.4: periférico; geralmente descarte se não passar nos filtros.

        ENTRADA:
        - Hoje: {data_hoje}
        - Itens (JSON): 
        {base_para_llm}

        SAÍDA (JSON array). Cada elemento deve seguir **exatamente** o schema abaixo (chaves em minúsculas):

        [
        {{
            "titulo": "<título original>",
            "achados_principais": [
            "<linha 1 com dado verificável>",
            "<linha 2>",
            "<linha 3>",
            "se a matéria for bastante relevante podem ter mais linhas"
            ],
            "por_que_importa": "<conectando a notícia ao setor de consórcios>",
            "fonte": "<nome da fonte>",
            "link": "<URL>",
            "data": "<DD-MM-AAAA>",
            "relevancia": 0.0
        }}
        ]

        Se **nenhum** item atender aos filtros, responda **[]**.

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
    
    









