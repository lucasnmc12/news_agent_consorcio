# from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper
from utils.llm_factory import get_llm
from datetime import datetime
from dotenv import load_dotenv
from utils.scraper import normalizar_e_dedup_links, enriquecer_com_texto_links

load_dotenv()

data_hoje = datetime.now().strftime('%d de %B de %Y') 

def _montar_corpus_para_llm(completos, parciais, preview_full=1200, preview_snip=300):
    """
    Constrói o conteúdo que a LLM vai ler, baseado no TEXTO EXTRAÍDO.
    Mantém formato simples e citável.
    """
    blocos = []
# Itens com TEXTO completo
    for it in completos:
        titulo = it.get("title") or it.get("titulo") or "(sem título)"
        fonte  = it.get("source") or it.get("fonte") or ""
        data   = it.get("date") or it.get("data") or ""
        link   = it.get("link") or ""
        texto  = (it.get("texto") or "").strip().replace("\r", " ")
        trecho = texto[:preview_full] + ("…" if len(texto) > preview_full else "")
        blocos.append(
            f"- Título: {titulo}\n"
            f"  Fonte: {fonte} | Data: {data}\n"
            f"  Link: {link}\n"
            f"  Conteúdo extraído (COMPLETO):\n  {trecho}\n"
        )

    # Itens só com SNIPPET
    for it in parciais:
        titulo = it.get("title") or it.get("titulo") or "(sem título)"
        fonte  = it.get("source") or it.get("fonte") or ""
        data   = it.get("date") or it.get("data") or ""
        link   = it.get("link") or ""
        snip   = (it.get("snippet") or "").strip().replace("\r", " ")
        trecho = snip[:preview_snip] + ("…" if len(snip) > preview_snip else "")
        blocos.append(
            f"- Título: {titulo}\n"
            f"  Fonte: {fonte} | Data: {data}\n"
            f"  Link: {link}\n"
            f"  Conteúdo extraído [SNIPPET]:\n  {trecho}\n"
        )

    return "\n".join(blocos)



def search_consorcios(state):
    """Busca e gera relatório sobre o mercado de consórcios"""
    query = "consorcios"

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
   - Se você não conseguir determinar a data com segurança, **descarte** o item.
2) **Fontes confiáveis apenas**: priorize domínios como ABAC, Valor Econômico, G1, Estadão, O Globo, Folha, Exame, CNN Brasil, InfoMoney, bcb.gov.br, IBGE, Ipea, B3. 
   - **Descarte** publieditoriais e similares (ex.: "especial-publicitário", "publieditorial", "DINO") e páginas de vídeo sem transcrição.
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
      "<linha 3>"
    ],
    "por_que_importa": "<1 linha conectando ao setor de consórcios>",
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

    # Guarda no state tanto os dados brutos enriquecidos quanto o resumo
    total = len(noticias); completos = len(completos)
    state["consorcios_enriquecidos"] = noticias
    state["search_consorcios"] = f"[consórcios] coletadas={total}, completas={completos}\n\n{result.content}"
    print(state["search_consorcios"])
    return state
    
    










    resumo_links = formatar_resultados_serper(noticias)

    data_execucao = datetime.now().strftime("%d/%m/%Y")


    prompt = f"""
        Data de execução do relatório: {data_execucao}

        Você é um analista econômico. Sua tarefa é ler o material abaixo (trechos e links de notícias sobre o mercado de consórcios no Brasil) e produzir APENAS um resumo executivo com os pontos mais relevantes da última semana.

        CONTEÚDO A ANALISAR:
        {resumo_links}

        REGRAS (aplique todas):
        - Considere SOMENTE notícias publicadas nos últimos 15 dias em fontes confiáveis (Valor, G1, Estadão, Exame, CNN Brasil, InfoMoney, ABAC, Banco Central). Se a data for anterior, ignore.
        - Descarte matérias patrocinadas/“Dino”, publieditoriais ou republicações; prefira a fonte original.
        - Elimine duplicatas (mesma pauta/mesmos dados com outra manchete); mantenha a versão mais completa e clara.
        - Destaque só o que muda decisão: crescimento/setor, comportamento do consumidor, mudanças regulatórias, Selic/BCB, fraudes, fusões/aquisições, tecnologia/operacional.
        - Seja factual e neutro. Sem opinião. Sem floreios. Sem reescrever o estilo da fonte.

        FORMATO DE SAÍDA (máx. 8 itens):
        Para cada item, use exatamente o bloco abaixo:
        ---
        - **Título**: <título original>
        - **Achados principais**: <2–3 linhas com dados/conclusões verificáveis (percentuais, valores, datas, órgãos)>
        - **Por que importa**: <1 linha conectando o fato ao setor de consórcios>
        - **Fonte**: <nome da fonte>
        - **Link**: <URL>
        - **Data**: <DD-MM-AAAA>
        ---

        Se não houver nada relevante/recente, responda apenas: "Sem novidades relevantes na última semana."
        """


    llm = get_llm("search")
    result = llm.invoke(prompt)
    state["search_consorcios"] = result.content
    print(result.content)
    return state
