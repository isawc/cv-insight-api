from fastapi import FastAPI

from app.routers import analyze

app = FastAPI(
    title="CV Insight API",
    description="Assistente técnico de análise e compatibilidade de currículos com IA.",
    version="1.0.0",
)

app.include_router(analyze.router)


@app.get("/")
def root():
    return {"mensagem": "CV Insight API no ar! Acesse /docs para a documentação."}
