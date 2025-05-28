from graph_definition import graph

# Cria uma instância do grafo
graph_id = "news_report_001"

# Inicializa o grafo 
inputs = {}
graph.invoke(inputs, graph_id=graph_id)

# O grafo vai pausar na revisão

# Se aprovado 
graph.send(
    graph_id=graph_id,
    input={
    "approved":True,
    "approved_content": "Aprovado, o texto está bom"
        }
    )

# Ou se quiser solicitar revisão

graph.send(
    graph_id=graph_id,
    input={
    "approved":False,
    "feedback": "Melhore a clareza e adicione mais dados sobre macroeconomia."
        }
    )