from typing import Literal

from pydantic import BaseModel, Field


class ResultadoAnalise(BaseModel):
    nivel_estimado: Literal["júnior", "pleno", "sênior"]
    pontos_fortes: list[str]
    pontos_de_melhoria: list[str]
    sugestoes: list[str]
    compatibilidade_vaga: int = Field(ge=0, le=100)
    resumo: str
