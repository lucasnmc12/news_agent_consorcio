from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY_LUCAS = os.getenv("GEMINI_API_KEY_LUCAS")

# Isso só para fins de verificação
#print("Usando credenciais de:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
print("Usando chave da API:", GEMINI_API_KEY_LUCAS[:10] + "..." if GEMINI_API_KEY_LUCAS else "Nenhuma chave encontrada")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY_LUCAS,
    temperature=0.1,
    convert_system_message_to_human=True
)

response = llm.invoke("Me diga 3 vantagens de usar a Vertex AI com o modelo Gemini.")
print("Resposta:")
print(response.content)

