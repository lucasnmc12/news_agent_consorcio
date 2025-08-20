# nodes/search_all.py
from datetime import datetime, date

from nodes.search_bcb import search_bcb
from nodes.search_consorcios import search_consorcios
from nodes.search_macro import search_macro


def safe_call(fn, state: dict, name: str) -> dict:
    """Executa um nó com tolerância a erro e anota status no state."""
    try:
        out = fn(state)
        state[f"{name}_status"] = "ok"
        return out if out is not None else state
    except Exception as e:
        state[f"{name}_error"] = str(e)
        state[f"{name}_status"] = "error"
        return state


def _parse_date_flex(s: str) -> date | None:
    """Aceita DD-MM-YYYY, DD/MM/YYYY, YYYY-MM-DD; retorna None se não parsear."""
    if not s:
        return None
    s = s.strip()
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            pass
    return None


def merge_llm_json(state: dict) -> tuple[list[dict], dict[str, list[dict]]]:
    """
    Une os JSONs da LLM e agrupa por tema, sem filtros adicionais.
    - dedup por `link` (assume link já normalizado nos nós filhos)
    - ordena dentro de cada grupo por relevancia desc e, como desempate, data desc
    - mantém ordem de grupos: bcb -> consorcios -> macro
    Retorna: (lista_achatada, dict_por_tema)
    """
    # ordem fixa dos grupos na saída achatada
    fontes = {
        "bcb":        state.get("bcb_llm_json") or [],
        "consorcios": state.get("consorcios_llm_json") or [],
        "macro":      state.get("macro_llm_json") or [],
    }

    vistos: set[str] = set()
    grupos: dict[str, list[dict]] = {k: [] for k in fontes.keys()}

    # 1) juntar e deduplicar
    for origem, itens in fontes.items():
        for it in itens:
            link = (it.get("link") or "").strip()
            if not link or link in vistos:
                continue
            novo = dict(it)
            novo.setdefault("origem", origem)
            grupos[origem].append(novo)
            vistos.add(link)

    # 2) ordenar dentro de cada grupo (relevancia desc, data desc como desempate)
    def _rel(x: dict) -> float:
        try:
            return float(x.get("relevancia", 0.0) or 0.0)
        except Exception:
            return 0.0

    def _data(x: dict) -> date:
        return _parse_date_flex(x.get("data", "") or "") or date.min

    for origem in grupos:
        grupos[origem].sort(key=lambda x: (_rel(x), _data(x)), reverse=True)

    # 3) lista achatada (grupos “colados”, na ordem bcb -> consorcios -> macro)
    unificada_flat: list[dict] = []
    for origem in fontes.keys():
        unificada_flat.extend(grupos[origem])

    return unificada_flat, grupos


def search_all(state: dict) -> dict:
    """Nó inicial: dispara buscas, unifica e agrupa para os próximos nós."""
    state = safe_call(search_bcb, state, "bcb")
    state = safe_call(search_consorcios, state, "consorcios")
    state = safe_call(search_macro, state, "macro")

    unificada_flat, por_tema = merge_llm_json(state)

    # disponibiliza para o merged_content
    state["news_unificadas_json"] = unificada_flat     # lista achatada (grupos juntos)
    state["news_por_tema"] = por_tema                  # dict agrupado por tema

    # status opcional (apenas contagens)
    c_json = len(state.get("consorcios_llm_json") or [])
    m_json = len(state.get("macro_llm_json") or [])
    b_json = len(state.get("bcb_llm_json") or [])
    state["search_all_status"] = (
        f"[ALL] bcb={b_json} | consorcios={c_json} | macro={m_json} | unificadas={len(unificada_flat)}"
    )

    return state

    

   



    
      







