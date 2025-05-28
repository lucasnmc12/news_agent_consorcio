from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv() # GROQ_API_KEY
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_CONFIG = {
    "search": "llama3-8b-8192",
    "merge": "llama3-70b-8192",
    "review": "mixtral-8x7b-32768",
    "formatting": "llama3-70b-8192"
}


def get_llm(task: str):
    """
    Retorna o modelo apropriado baseado na tarefa.
    :param task: search, merge, review, formatting
    :return: Instância da LLM configurada
    """
    model = LLM_CONFIG.get(task, "llama3-70b-8192") # Default  segurança
    return ChatGroq(
        api_key = GROQ_API_KEY,
        model_name = model
    )
