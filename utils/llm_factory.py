from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv() # GROQ_API_KEY
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_KEY2 = os.getenv("GOOGLE_API_KEY2")


LLM_CONFIG = {
    "search": "gemini-1.5-flash",
    "merge": "gemini-1.5-flash",
    "review": "gemini-1.5-flash",
    "formatting": "gemini-1.5-flash"
}


def get_llm(task: str):
    """
    Retorna o modelo apropriado baseado na tarefa.
    :param task: search, merge, review, formatting
    :return: Instância da LLM configurada via Vertex AI
    """
    model = LLM_CONFIG.get(task, "gemini-1.5-flash")
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=GOOGLE_API_KEY2,
        temperature=0.1,
        convert_system_message_to_human=True  # evita warnings
    #   location="us-central1",  # ou outro conforme configuração do projeto
    )
