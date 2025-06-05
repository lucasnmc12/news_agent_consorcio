import requests
import os

def buscar_noticias_google(query):
    api_key = os.getenv("GOOGLE_API_KEY2")
    cx = os.getenv("GOOGLE_SEARCH_ENGINE_ID")  # ID do mecanismo de busca
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": api_key,
        "cx": cx,
        "q": query
    }

    response = requests.get(url, params=params)
    return response.json()
