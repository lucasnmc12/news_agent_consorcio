from nodes.search_bcb import search_bcb  # ou ajuste o nome do arquivo
state = {}
state = search_bcb(state)
print("\n📄 Resultado do relatório:\n")
print(state["search_bcb"])