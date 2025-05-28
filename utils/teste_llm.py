from llm_factory import get_llm

llm = get_llm("search")
res = llm.invoke("Me dê um resumo das últimas notícias sobre o Banco Central do Brasil.")
print (res)