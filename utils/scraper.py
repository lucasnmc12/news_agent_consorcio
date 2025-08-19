from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import requests
import trafilatura



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