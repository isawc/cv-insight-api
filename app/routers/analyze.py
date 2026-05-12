from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.ai_analyzer import analisar_curriculo
from app.pdf_extractor import extrair_texto_pdf

router = APIRouter(prefix="/analyze", tags=["Análise de Currículo"])

TAMANHO_MAXIMO_BYTES = 10 * 1024 * 1024


@router.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok", "mensagem": "CV Insight API funcionando!"}


@router.post("/", summary="Analisar currículo")
async def analisar(
    arquivo: UploadFile = File(...),
    descricao_vaga: Optional[str] = Form(default=""),
):
    if not arquivo.filename or not arquivo.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos PDF são aceitos.",
        )

    conteudo = await arquivo.read()

    if len(conteudo) > TAMANHO_MAXIMO_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Arquivo muito grande. O limite é 10 MB.",
        )

    try:
        texto = extrair_texto_pdf(conteudo)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro)) from erro

    try:
        return analisar_curriculo(texto, descricao_vaga)
    except ValueError as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro
