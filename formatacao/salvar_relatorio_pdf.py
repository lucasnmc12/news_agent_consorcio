# salvar_relatorio_pdf.py
import os
from datetime import datetime
from markdown import markdown
from weasyprint import HTML

# Criação automática das pastas se não existirem
os.makedirs("results/results_md", exist_ok=True)
os.makedirs("results/results_pdf", exist_ok=True)

def salvar_como_markdown(conteudo, nome_arquivo="relatorio.md"):
    caminho = os.path.join("results", "results_md", nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"✅ Markdown salvo em: {caminho}")

def converter_md_para_html(nome_arquivo_md="relatorio.md"):
    caminho_md = os.path.join("results", "results_md", nome_arquivo_md)
    with open(caminho_md, "r", encoding="utf-8") as f:
        md_text = f.read()

         # Converte Markdown para HTML
    html_conteudo = markdown(md_text)

    # Insere no template com estilo
    html_final = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Relatório</title>
      <style>
        body {{
          font-family: 'Lato', sans-serif;
          margin: 40px;
          color: #333;
          line-height: 1.6;
          font-size: 12px;
        }}
        h1 {{
      color: #202E5F;
      margin-bottom: 10px;
      font-size: 20px; /* título principal */
        }}
        h2 {{
          color: #202E5F;
          margin-bottom: 10px;
          font-size: 16px; /* subtítulo */
        }}
        h3 {{
          color: #202E5F;
          margin-bottom: 10px;
          font-size: 14px; /* subtítulo menor */
        }}
            a {{
              color: #202E5F;
              text-decoration: none;
            }}
        a:hover {{
          text-decoration: underline;
        }}
        p {{
          margin-bottom: 15px;
        }}
      </style>
    </head>
    <body>
      {html_conteudo}
    </body>
    </html>
    """

    return html_final

def salvar_pdf(html_content, nome_arquivo=None):
    if nome_arquivo is None:
        data_hoje = datetime.now().strftime("%d-%m-%Y")
        nome_arquivo = f"relatorio_{data_hoje}.pdf"
        
    caminho_pdf = os.path.join("results", "results_pdf", nome_arquivo)
    HTML(string=html_content).write_pdf(caminho_pdf)
    print(f"✅ PDF salvo em: {caminho_pdf}")