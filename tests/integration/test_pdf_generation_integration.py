import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from salvar_relatorio_pdf import salvar_como_markdown, converter_md_para_html, salvar_pdf


def test_pdf_generation(tmp_path):
    # 🚀 Definir nomes de arquivos temporários
    nome_md = "test_relatorio.md"
    nome_pdf = "test_relatorio.pdf"

    # 🚧 Gerar Markdown (✅ sem identação!)
    conteudo = (
        "# Relatório de Teste\n"
        "Este é um relatório de teste para validar a geração de PDF a partir de Markdown.\n"
    )

    salvar_como_markdown(conteudo, nome_md)

    # 🔍 Verificar se o arquivo MD foi criado
    caminho_md = os.path.join("results", "results_md", nome_md)
    assert os.path.exists(caminho_md)

    # 🧠 Converter para HTML
    html_content = converter_md_para_html(nome_md)
    assert "<h1>Relatório de Teste</h1>" in html_content

    # 🗎 Salvar PDF
    salvar_pdf(html_content, nome_pdf)

    # ✅ Verificar se o PDF foi criado
    caminho_pdf = os.path.join("results", "results_pdf", nome_pdf)
    assert os.path.exists(caminho_pdf)
    assert os.path.getsize(caminho_pdf) > 0  # Verifica se o PDF não está vazio