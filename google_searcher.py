import requests
import os

print

def buscar_noticias_google(query):
    api_key = os.getenv("GOOGLE_SEARCH_API")
    cx = os.getenv("GOOGLE_SEARCH_ENGINE_ID")  # ID do mecanismo de busca
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": api_key,
        "cx": cx,
        "q": query
    }

    response = requests.get(url, params=params)
    #return response.json()
    results = response.json()
    print (results)

buscar_noticias_google("quem é messi?")
