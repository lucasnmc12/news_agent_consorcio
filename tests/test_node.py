import os, sys, json, re
from datetime import datetime
from utils.scraper import _extrair_primeiro_json_array

# ajuste se necessário
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nodes.search_consorcios import search_consorcios
from nodes.search_bcb import search_bcb
from nodes.search_macro import search_macro


def _extrair_json_da_resposta(resp_str: str):
    # seu nó grava: "[consórcios] ...\n\n{JSON}"
    # Pega o primeiro bloco JSON (de [ até ]).
    if not resp_str:
        return []
    start = resp_str.find('[')
    end   = resp_str.rfind(']')
    if start == -1 or end == -1 or end <= start:
        return []
    try:
        return json.loads(resp_str[start:end+1])
    except Exception:
        return []

def main():
    # verificação mínima de env
    assert os.getenv("SERPER_API_KEY"), "SERPER_API_KEY ausente no ambiente/.env"

    state = {}
    out = search_consorcios(state)

    # 1) conferências básicas
    assert "consorcios_enriquecidos" in out, "Faltou consorcios_enriquecidos no state"
    assert "search_consorcios" in out, "Faltou search_consorcios no state"

    itens = out["consorcios_enriquecidos"]
    print(f"[LIVE] Itens enriquecidos: {len(itens)}")
    completos = sum(1 for i in itens if i.get("texto_completo"))
    print(f"[LIVE] Com texto completo: {completos}/{len(itens)}")

    # 2) extrai o JSON que a LLM retornou
    #resposta = out["search_consorcios"]
    parsed = out.get("consorcios_llm_json", [])
    # fallback: tentar parsear do RAW se vier vazio/None
    if not parsed:
        raw = out.get("consorcios_llm_raw", "")
        parsed = _extrair_primeiro_json_array(raw)  # mesma função sanitizadora usada no nó
    print(f"[LIVE] Itens no JSON final: {len(parsed)}")

    # 3) valida o schema mínimo por item
    for k, item in enumerate(parsed, 1):
        for campo in ["titulo", "achados_principais", "por_que_importa", "fonte", "link", "data", "relevancia"]:
            assert campo in item, f"Campo {campo} ausente no item {k}"
        assert isinstance(item["achados_principais"], list) and (1 <= len(item["achados_principais"]) <= 5)
        assert isinstance(item["relevancia"], (int, float)) and 0.0 <= float(item["relevancia"]) <= 1.0

    # 4) snapshots para auditoria
    os.makedirs("tests/_artifacts", exist_ok=True)
    with open("tests/_artifacts/consorcios_enriquecidos_live.json", "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False, indent=2)
    with open("tests/_artifacts/consorcios_llm_live.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)
    with open("tests/_artifacts/consorcios_llm_raw.txt", "w", encoding="utf-8") as f:
        f.write(out.get("consorcios_llm_raw", ""))

    print("Snapshots salvos em tests/_artifacts/consorcios_*.json")

if __name__ == "__main__":
    main()
