import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.llm_factory import get_llm

def test_get_llm_returns_model_for_valid_task():
    model = get_llm('search')
    assert model is not None
    assert hasattr(model, 'invoke') or hasattr(model, 'generate_content')

def test_get_llm_returns_model_for_unknown_task():
    model = get_llm('unknown_task')
    assert model is not None
    assert hasattr(model, 'invoke') or hasattr(model, 'generate_content')

def test_get_llm_returns_same_model_for_different_tasks():
    tasks = ['search', 'merge', 'review', 'formatting']
    for task in tasks:
        model = get_llm(task)
        assert model is not None
        assert hasattr(model, 'invoke') or hasattr(model, 'generate_content')
