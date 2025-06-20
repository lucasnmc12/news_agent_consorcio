FROM python:3.12-slim

WORKDIR /app

# ✅ Instala dependências de sistema para WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libjpeg-dev \
    libxml2 \
    libxslt1-dev \
    zlib1g-dev \
    libglib2.0-0 \
    fonts-liberation \
    fonts-dejavu \
    && apt-get clean

# Copia os arquivos
COPY . .

# ✅ Instala o uv usando o pip do sistema
RUN pip install --no-cache-dir uv

# ✅ Instala as dependências do pyproject.toml diretamente no sistema (sem .venv)
RUN uv pip install --system --no-cache-dir .

# ✅ Cria diretórios necessários
RUN mkdir -p results/results_md results/results_pdf

# ✅ Porta exposta (opcional se for Streamlit ou API)
EXPOSE 8501

# ✅ Comando de execução
# Se usar Streamlit:
# CMD ["streamlit", "run", "main.py"]

# Ou se for script Python direto:
CMD ["python", "main.py"]
