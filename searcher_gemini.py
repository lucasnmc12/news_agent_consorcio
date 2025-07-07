import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import os
import re

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY_LUCAS")
genai.configure(api_key=api_key)


def buscar_noticias_gemini(query: str) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",  # ou gemini-2.5-pro se sua conta tiver acesso
        tools=[{"google_search": {}}]
    )

    prompt = f"""
    Hoje é {datetime.now().strftime('%d/%m/%Y')}.
    Pesquise na web (usando a ferramenta de busca) notícias de até no máximo 8 dias desde a sua publicação sobre: {query}.
    Essas notícias serão utilizadas em um **relatório corporativo** para uma empresa do setor de consórcios, portanto devem conter **informações úteis para análise estratégica**, como:
    - comportamento do mercado
    - inadimplência
    - crescimento do setor
    - mudanças regulatórias
    - impacto da Selic
    - ações do Banco Central ou da ABAC
    - fraudes ou problemas estruturais no setor
    Use fontes confiáveis como g1.globo.com, valor.globo.com, cnnbrasil.com.br, exame.com, oglobo.globo.com, estadao.com.br, abac.org.br e bcb.gov.br.
    
    O objetivo é apenas retornar as notícias de forma fiel e detalhada, como foram publicadas pelas fontes.

    Para cada notícia:
    - Forneça o **título original**
    - Um **resumo completo e fiel ao conteúdo publicado**, sem reescrever ou adaptar o estilo
    - A **fonte original** (ex: G1, Valor Econômico, Exame, etc.)
    - E o **link direto** da notícia
    
    Responda diretamente no formato abaixo:
    ---
    - **Título**: ...
    - **Conteúdo**: ...
    - **Fonte**: ...
    - **Link**: ...
    ---
    """

    response = model.generate_content(contents=prompt)
    texto_final = "\n".join(part.text for part in response.parts)
    return texto_final
    



