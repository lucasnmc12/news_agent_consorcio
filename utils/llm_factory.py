from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv() # GROQ_API_KEY
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY_LUCAS")



LLM_CONFIG = {
    "search": "gemini-1.5-flash",
    "merge": "gemini-1.5-flash",
    "review": "gemini-1.5-flash",
    "formatting": "gemini-1.5-flash"
}


def get_llm(task: str):
    model = LLM_CONFIG.get(task, "gemini-1.5-flash")
    api_key = GEMINI_API_KEY

    if api_key is None:
        raise Exception("🚨 GEMINI_API_KEY não encontrado. Verifique seu arquivo .env!")

    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=0.1,
        convert_system_message_to_human=True
    )
