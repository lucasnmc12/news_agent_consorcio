import sys
import os
from utils.scraper import normalizar_url, baixar_html, extrair_texto

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper, buscar_noticias_serper_bacen

noticias = buscar_noticias_serper("mercado de consorcio", max_results=3)

vistos = set()
limpas = []

for it in noticias:
        raw = it.get("link")
        if not raw:
                continue
        clean = normalizar_url(raw)
        if not clean or clean in vistos:
            continue
        vistos.add(clean)
        it["link_original"] = raw
        it["link"] = clean
        limpas.append(it)

print(f"Coletadas: {len(noticias)} | Após normalização/dedup: {len(limpas)}")


min_chars = 400
enriquecidas = []
for i in limpas:

        html = baixar_html(i.get("link"))
        url_usada = i.get("link") # usar a limpa por padrao

        # fallback se a url limpa nao funcionar
        if not html and i.get("link_original"): 
               html = baixar_html(i.get("link_original"))
               if html:
                      url_usada = i.get("link_original")


        texto = extrair_texto(html, url_usada) if html else None
        if not texto or len(texto) < min_chars:
               texto = (i.get("snippet")or "").strip()
        i["texto"] = texto
        i["texto_completo"] = len(texto) >= min_chars
        i["scrape_url_usada"] = url_usada      # opcional: útil pra debug


        enriquecidas.append(i)

completas = sum(1 for x in enriquecidas if x["texto_completo"])
print(f"Com texto completo: {completas}/{len(enriquecidas)}")

# visualização detalhada (todos os itens; ajuste preview_chars se quiser)
preview_chars = 600
for j, it in enumerate(enriquecidas, 1):
    titulo = it.get("title") or it.get("titulo") or "(sem título)"
    link_limpo = it.get("link", "")
    scrape_url = it.get("scrape_url_usada") or link_limpo
    fonte = it.get("source") or it.get("fonte") or ""
    data = it.get("date") or it.get("data") or ""
    texto = (it.get("texto") or "").strip()

    preview = texto[:preview_chars].replace("\n", " ")
    if len(texto) > preview_chars:
        preview += "…"

    print("\n" + "="*88)
    print(f"[{j}] {titulo}")
    print(f"Fonte/Data  : {fonte} | {data}")
    print(f"Link (limpo): {link_limpo}")
    print(f"Scrape URL  : {scrape_url}")     # <- URL realmente usada no scraping
    print(f"Texto OK?   : {it.get('texto_completo')} | len(texto) = {len(texto)}")
    print(f"Preview     : {preview}")

# This code is for testing the news scraping functionality, specifically for consortia news.