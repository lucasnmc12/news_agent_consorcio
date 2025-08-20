from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import requests
import trafilatura
from typing import List, Dict, Tuple, Optional
import re, json




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

def _extrair_primeiro_json_array(s: str):
    if not s: return []
    # remove cercas de código
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s.strip(), flags=re.MULTILINE)
    # pega o primeiro bloco [...]
    a, b = s.find("["), s.rfind("]")
    if a == -1 or b == -1 or b <= a:
        return []
    js = s[a:b+1]
    # conserta vírgula antes de ] ou }
    js = re.sub(r",\s*(\]|\})", r"\1", js)
    try:
        return json.loads(js)
    except Exception:
        return []
