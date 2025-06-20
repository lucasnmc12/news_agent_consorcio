import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from graph_definition import workflow
import pytest


def test_graph_definition_execution():
    # 🏁 Estado inicial simula uma busca sobre "OpenAI"
    initial_state = {"query": "OpenAI"}

    # 🚀 Executa o workflow inteiro
    app = workflow.compile()

    try:
        for event in app.stream(initial_state):
            for key, value in event.items():
                print(f"[{key}] → {value}")
                last_state = value  # Guarda o último estado retornado
    except Exception as e:
        pytest.fail(f"O fluxo falhou com erro: {e}")

    # ✅ Verificações após finalização do fluxo
    assert last_state is not None
    assert "output" in last_state or "result" in last_state or "conteudo" in last_state

    # Se o fluxo tem campos específicos ao final, pode verificar:
    assert last_state.get("approved") is True or last_state.get("approved") is False
    assert isinstance(last_state.get("conteudo", []), list)
