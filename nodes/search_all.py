from nodes.search_bcb import search_bcb
from nodes.search_consorcios import search_consorcios
from nodes.search_macro import search_macro
#from nodes.search_generic import search_generic
from datetime import datetime, date
from urllib.parse import urlparse, urlunparse


def safe_call(fn, state: dict, name: str) -> dict:
    """
    Executa um nó com tolerância a erro.
    - Em caso de exceção: registra <name>_error e <name>_status="error", e devolve o state original.
    - Em caso de sucesso: devolve o state retornado pelo nó (ou o mesmo state, se o nó mutar in-place).
    """

    try:
        out = fn(state)
        state[f"{name}_status"] = "ok"
        return out if out is not None else state
    except Exception as e:
        state[f"{name}_error"] = str(e)
        state[f"{name}_status"] = "error"
        return state    
    

def merge_llm_json(
    state: dict,
    max_age_days: int | None = 16,
    group_order_metric: str = "max",   # "max" (padrão) ou "avg"
) -> list[dict]:
    """
    Une consorcios_llm_json + macro_llm_json + bcb_llm_json:
      - adiciona campo 'origem' (consorcios|macro|bcb)
      - deduplica por link normalizado (scheme/host/path; ignora query/fragment)
      - opcional: filtra por data ≤ max_age_days (campo 'data' no formato DD-MM-AAAA)
      - opcional: ordena por (relevancia desc, data desc)
    """

    def _parse_dd_mm_aaaa(s: str) -> date | None:
        try:
            return datetime.strptime(s, "%d-%m-%Y").date()
        except Exception:
            return None
        
    def _is_within_days(d: date, days: int) -> bool:
        if not d:
            return False
        return 0 <= (date.today() - d).days <= days

    fontes = {
        "consorcios": state.get("consorcios_llm_json") or [],
        "macro":      state.get("macro_llm_json") or [],
        "bcb":        state.get("bcb_llm_json") or [],
    }
        
    # 1) filtra + dedup por link

    vistos: set[str] = set()
    grupos: dict[str, list[dict]] = {"consorcios": [], "macro": [], "bcb": []}

    for origem, itens in fontes.items():
        for it in itens:
            link = (it.get("link") or "").strip()
            if not link or link in vistos:
                continue

        if max_age_days is not None:
            d = _parse_dd_mm_aaaa(it.get("data", "") or "")
            if not d or not _is_within_days(d, max_age_days):
                continue

        novo = dict(it)
        novo.setdefault("origem", origem)
        grupos[origem].append(novo)
        vistos.add(link)

        # 2) ordena itens dentro de cada grupo (relevancia desc, data desc)
    def _rel(x: dict) -> float:
        try:
            return float(x.get("relevancia", 0.0) or 0.0)
        except Exception:
            return 0.0
        

    def _data(x: dict) -> date:
        return _parse_dd_mm_aaaa(x.get("data", "") or "") or date.min

    for origem in grupos:
        grupos[origem].sort(key=lambda x: (_rel(x), _data(x)), reverse=True)


    # 3) decide ordem dos grupos (por métrica do grupo)
    def _grupo_score(items: list[dict]) -> float:
        if not items:
            return -1.0
        vals = [_rel(x) for x in items]
        return max(vals) if group_order_metric == "max" else (sum(vals) / max(len(vals), 1))

    ordem_grupos = sorted(grupos.keys(), key=lambda g: _grupo_score(grupos[g]), reverse=True)


    # 4) concatena grupos na ordem escolhida
    merged: list[dict] = []
    for g in ordem_grupos:
        merged.extend(grupos[g])

    return merged


def search_all(state: dict) -> dict:
    state = safe_call(search_bcb, state, "bcb")
    state = safe_call(search_consorcios, state, "consorcios")
    state = safe_call(search_macro, state, "macro")

    unificadas = merge_llm_json(state, max_age_days=16, group_order_metric="max")
    state["news_unificadas_json"] = unificadas


    # status opcional
    c_tot  = len(state.get("consorcios_enriquecidos", []))
    c_json = len(state.get("consorcios_llm_json", []) or [])
    m_tot  = len(state.get("macro_enriquecidos", []))
    m_json = len(state.get("macro_llm_json", []) or [])
    b_tot  = len(state.get("bcb_enriquecidos", []))
    b_json = len(state.get("bcb_llm_json", []) or [])
    state["search_all_status"] = (
        f"[ALL] consórcios {c_tot}/{c_json} | macro {m_tot}/{m_json} | bcb {b_tot}/{b_json} | unificadas {len(unificadas)}"
    )
    return state


    

    

   



    
      







