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
    Pesquise na web (usando a ferramenta de busca) sobre: {query}.
    Use fontes confiáveis como g1.globo.com, valor.globo.com, cnnbrasil.com.br, exame.com, oglobo.globo.com, estadao.com.br, abac.org.br e bcb.gov.br.
    
    Para cada uma das 3 notícias mais relevantes:
    - Forneça um **título**
    - Um **resumo profissional e informativo**
    - A **fonte (ex: G1, Valor Econômico)**
    - E o **link da notícia**.
    
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
    



