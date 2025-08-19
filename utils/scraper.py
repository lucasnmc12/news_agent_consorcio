from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import requests
import trafilatura
from typing import List, Dict, Tuple, Optional




def normalizar_url(u:str) -> str:

    if not u:
        return ""
    p = urlparse(u)

    # remove utm_* e parâmetros vazios repetidos
    clean_qs = [
        (k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
        if not k.lower().startswith("utm_")
    ]

    # remove barra final do path (evita duplicata /noticia e /noticia/)
    path = p.path.rstrip("/")

    # reconstrói a URL “limpa”
    return urlunparse((p.scheme, p.netloc, path, p.params, urlencode(clean_qs), ""))



UA = {"User-Agent": "Mozilla/5.0 (ReportBot/1.0; +https://example.com/bot)"}

def baixar_html(url:str, timeout=15) -> str | None:
    try:
        resp = requests.get(url, headers = UA, timeout = timeout)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        return None
    
def extrair_texto(html: str, url: str) -> str | None:

    if not html:
        return None
    texto = trafilatura.extract(
        html,
        url=url,
        include_images=False,
        include_comments=False,
        favor_recall=True
    )
    return texto.strip() if texto else None


def normalizar_e_dedup_links(noticias: List[Dict]) -> List[Dict]:
    """
    Recebe itens do Serper (com chave 'link') e:
      - normaliza a URL
      - remove duplicatas por URL normalizada
      - preserva `link_original` quando diferente
    Retorna nova lista com os itens válidos.
    """
    vistos = set()
    out: List[Dict] = []
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
        out.append(it)
    return out


def baixar_html_com_fallback(item: Dict) -> Tuple[Optional[str], Optional[str]]:
    """
    Tenta baixar HTML usando primeiro `link` (limpo) e,
    se falhar, tenta `link_original`. Retorna (html, url_usada).
    """
    # 1) tenta link limpo
    url = item.get("link")
    html = baixar_html(url) if url else None
    if html:
        return html, url

    # 2) fallback: link_original
    url_orig = item.get("link_original")
    if url_orig:
        html2 = baixar_html(url_orig)
        if html2:
            return html2, url_orig

    return None, None

def enriquecer_com_texto_links(
    noticias: List[Dict],
    min_chars: int = 400,
) -> List[Dict]:
    """
    Para cada item:
      - baixa HTML (com fallback para link_original)
      - extrai texto com trafilatura
      - se não atingir `min_chars`, cai para o snippet
      - marca `texto_completo` e `scrape_url_usada`
    Retorna nova lista (itens são mutados in-place).
    """
    out: List[Dict] = []
    for it in noticias:
        # baixa html (limpo → original)
        html, url_usada = baixar_html_com_fallback(it)

        # extrai texto
        texto = extrair_texto(html, url_usada) if html else None

        # fallback: usa snippet se curto/ausente
        if not texto or len(texto) < min_chars:
            texto = (it.get("snippet") or "").strip()

        it["texto"] = texto
        it["texto_completo"] = len(texto) >= min_chars
        it["scrape_url_usada"] = url_usada or it.get("link")  # para debug

        out.append(it)
    return out


def debug_imprimir_noticias(
    itens: List[Dict],
    n: int = 5,
    preview_chars: int = 600,
    somente_completos: bool = False,
) -> None:
    """
    Visualização rápida dos itens enriquecidos.
    """
    count = 0
    for idx, it in enumerate(itens, 1):
        if somente_completos and not it.get("texto_completo"):
            continue

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
        print(f"[{idx}] {titulo}")
        print(f"Fonte/Data  : {fonte} | {data}")
        print(f"Link (limpo): {link_limpo}")
        print(f"Scrape URL  : {scrape_url}")
        print(f"Texto OK?   : {it.get('texto_completo')} | len(texto) = {len(texto)}")
        print(f"Preview     : {preview}")

        count += 1
        if count >= n:
            break
