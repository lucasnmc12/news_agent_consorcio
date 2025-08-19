import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.search_serper import buscar_noticias_serper, formatar_resultados_serper

noticias = buscar_noticias_serper("consórcios")
print(formatar_resultados_serper(noticias))
