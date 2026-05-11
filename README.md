# CV Insight API

Assistente técnico de análise e compatibilidade de currículos com IA.

Projeto desenvolvido para praticar integração com APIs de IA, 
processamento de arquivos PDF e boas práticas de desenvolvimento em Python.

## O que faz

- Recebe um currículo em PDF
- Extrai e processa o texto automaticamente
- Analisa com IA (Claude da Anthropic)
- Retorna um relatório técnico em JSON com:
  - Pontos fortes identificados
  - Pontos de melhoria
  - Nível estimado (júnior / pleno / sênior)
  - Compatibilidade com uma vaga informada (0–100%)
  - Sugestões objetivas de melhoria

## Tecnologias

- Python 3.12
- FastAPI
- PyPDF2
- Anthropic API (Claude)
- Railway (deploy)

## Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/isawc/cv-insight-api.git
cd cv-insight-api

# Crie e ative o ambiente virtual
py -3.12 -m venv venv
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com sua chave da API Anthropic

# Rode o servidor
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

## Status

🚧 Em desenvolvimento