import sys
import os
from utils.scraper import normalizar_url, baixar_html, extrair_texto

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper, buscar_noticias_serper_bacen

noticias = buscar_noticias_serper("Consorcios", max_results=3)


print(formatar_resultados_serper(noticias))
