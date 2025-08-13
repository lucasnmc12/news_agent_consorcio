# from utils.search_ddgs import buscar_noticias, formatar_resultados
from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper
from searcher_gemini import buscar_noticias_gemini
from utils.llm_factory import get_llm
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

mes_atual = datetime.now().strftime('%B %Y')  # Junho 2025

def search_consorcios(state):
    """Busca e gera relatório sobre o mercado de consórcios"""
    query = "mercado de consórcios últimas notícias Brasil"

    noticias = buscar_noticias_serper(query)

    if not noticias:
        mensagem = "⚠️ Nenhuma notícia encontrada sobre consórcios."
        print(mensagem)
        return {"search_consorcios": mensagem}

    resumo_links = formatar_resultados_serper(noticias)

    data_execucao = datetime.now().strftime("%d/%m/%Y")


    prompt = f"""
        Data de execução do relatório: {data_execucao}

        Você é um analista econômico. Sua tarefa é ler o material abaixo (trechos e links de notícias sobre o mercado de consórcios no Brasil) e produzir APENAS um resumo executivo com os pontos mais relevantes da última semana.

        CONTEÚDO A ANALISAR:
        {resumo_links}

        REGRAS (aplique todas):
        - Considere SOMENTE notícias publicadas nos últimos 8 dias em fontes confiáveis (Valor, G1, Estadão, Exame, CNN Brasil, InfoMoney, ABAC, Banco Central). Se a data for anterior, ignore.
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
        - **Data**: <AAAA-MM-DD>
        ---

        Se não houver nada relevante/recente, responda apenas: "Sem novidades relevantes na última semana."
        """


    llm = get_llm("search")
    result = llm.invoke(prompt)
    state["search_consorcios"] = result.content
    print(result.content)
    return state
