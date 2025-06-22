📰 News Agent

Agente de geração de relatórios de notícias utilizando inteligência artificial e APIs de busca. O projeto realiza buscas na internet, faz resumo inteligente dos conteúdos e gera relatórios em PDF, seguindo fluxo de revisão e formatação editorial.



🚀 Funcionalidades

🔍 Busca de notícias em fontes confiáveis usando a API Serper.dev.

🤖 Processamento e resumo inteligente com Google Gemini API (via LangChain).

✍️ Revisão assistida por IA ou por humanos (Human-in-the-loop).

📝 Formatação editorial do conteúdo.

📄 Geração de relatórios em PDF e Markdown.

🔗 Workflow de execução controlado com LangGraph.



🐳 Executável via Docker para garantir ambiente padronizado.

🗂️ Estrutura do Projeto


news-agent/
├── nodes/                 # Lógica dos nós da LangGraph
├── utils/                 # Funções utilitárias (busca, LLM, etc.)
├── output/                # Outputs intermediários
├── results/               # Relatórios gerados (PDF e Markdown)
├── tests/                 # Testes unitários, integração e aceitação
├── .github/workflows/     # Pipeline CI/CD
├── Dockerfile             # Definição da imagem Docker
├── pyproject.toml         # Gerenciamento de dependências com UV
├── main.py                # Arquivo principal de execução
└── README.md              # Documentação do projeto



⚙️ Tecnologias Utilizadas
🐍 Python 3.12

🚀 LangChain + LangGraph

🤖 Google Gemini API

🔍 Serper.dev API

📦 Docker

🔧 uv (gerenciador de dependências moderno)

✅ pytest (testes automatizados)

🧾 WeasyPrint (geração de PDF)

🔗 GitHub Actions (pipeline CI/CD)



🐳 Como Executar com Docker
1️⃣ Crie um arquivo .env com suas chaves:

env

SERPER_API_KEY=xxxx
GOOGLE_API_KEY=xxxx
GROQ_API_KEY=xxxx
TAVILY_API_KEY=xxxx



2️⃣ Build da imagem Docker:

docker build -t news-agent .



3️⃣ Executar o container:

docker run --env-file .env -v ${PWD}/results:/app/results -it --rm news-agent



🧪 Executar os Testes
🐍 Localmente (ambiente Python):

pytest tests/unit
pytest tests/integration
pytest tests/acceptance



🐳 Com Docker (se configurado para testes):

docker run --env-file .env -it --rm news-agent pytest tests



🔄 Pipeline CI/CD

✔️ Build automático no GitHub Actions.

✔️ Execução de testes de unidade, integração e aceitação.

✔️ Build da imagem Docker.

✔️ Validação do ambiente e geração de relatórios.



🔑 Variáveis de Ambiente

Nome	Descrição
SERPER_API_KEY	Chave da API Serper.dev
GOOGLE_API_KEY	Chave da API Google Gemini
GROQ_API_KEY	(Opcional) Chave da API Groq
TAVILY_API_KEY	(Opcional) Chave da API Tavily

