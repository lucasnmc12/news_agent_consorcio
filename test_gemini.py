from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY2 = os.getenv("GOOGLE_API_KEY2")

# Isso só para fins de verificação
#print("Usando credenciais de:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
print("Usando chave da API:", GOOGLE_API_KEY2[:10] + "..." if GOOGLE_API_KEY2 else "Nenhuma chave encontrada")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY2,
    temperature=0.1,
    convert_system_message_to_human=True
)

response = llm.invoke("Me diga 3 vantagens de usar a Vertex AI com o modelo Gemini.")
print("Resposta:")
print(response.content)

