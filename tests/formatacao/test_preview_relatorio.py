import os
import webbrowser
from markdown import markdown

# Caminho absoluto do diretório base do projeto
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", ".."))

# Caminho do Markdown absoluto
caminho_md = os.path.join(base_dir, "results", "results_md", "relatorio_21-07-2025.md")  # ajuste o nome se necessário

# Caminho de saída do HTML
caminho_preview = "preview_relatorio.html"

# Lê e converte o conteúdo do .md para HTML
with open(caminho_md, "r", encoding="utf-8") as f:
    md_content = f.read()

html_conteudo = markdown(md_content)

# Template HTML com estilo embutido
html_template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Prévia do Relatório</title>
  <style>
    body {{
      font-family: 'Segoe UI', Tahoma, sans-serif;
      margin: 40px;
      color: #333;
      line-height: 1.6;
    }}
    h1, h2, h3 {{
      color: #202E5F;
      margin-bottom: 0.5em;
    }}
    a {{
      color: #202E5F;
      text-decoration: none;
      font-weight: bold;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    p {{
      margin-bottom: 15px;
    }}
    ul {{
      margin-left: 20px;
    }}
  </style>
</head>
<body>
  {html_conteudo}
</body>
</html>
"""

# Salva o HTML
with open(caminho_preview, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"✅ Prévia salva em: {caminho_preview}")

# Abre automaticamente no navegador padrão
webbrowser.open(f"file://{os.path.abspath(caminho_preview)}")
