import json

from typing import Literal

from pydantic import BaseModel, Field


class ResultadoAnalise(BaseModel):
    nivel_estimado: Literal["júnior", "pleno", "sênior"]
    pontos_fortes: list[str]
    pontos_de_melhoria: list[str]
    sugestoes: list[str]
    compatibilidade_vaga: int = Field(ge=0, le=100)
    resumo: str


from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL, MAX_TOKENS

cliente = Groq(api_key=GROQ_API_KEY)


def analisar_curriculo(texto_curriculo: str, descricao_vaga: str = "") -> dict:
    contexto_vaga = (
        f"""
Vaga para análise de compatibilidade:
{descricao_vaga}
"""
        if descricao_vaga
        else ""
    )

    prompt = f"""
Você é um assistente técnico especializado em análise de currículos de tecnologia.
Analise o currículo abaixo e retorne APENAS um JSON válido, sem nenhum texto antes ou depois.

{contexto_vaga}

Currículo:
{texto_curriculo}

Retorne exatamente neste formato:
{{
    "nivel_estimado": "júnior | pleno | sênior",
    "pontos_fortes": ["ponto 1", "ponto 2", "ponto 3"],
    "pontos_de_melhoria": ["ponto 1", "ponto 2", "ponto 3"],
    "sugestoes": ["sugestão 1", "sugestão 2", "sugestão 3"],
    "compatibilidade_vaga": 0,
    "resumo": "resumo objetivo em 2 linhas"
}}

Regras:
- compatibilidade_vaga deve ser um número de 0 a 100
- Se nenhuma vaga foi informada, compatibilidade_vaga deve ser 0
- Seja objetivo e técnico nas análises
- Retorne APENAS o JSON, sem markdown, sem explicações
"""

    resposta = cliente.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )

    texto_resposta = resposta.choices[0].message.content

    if not texto_resposta:
        raise ValueError("A IA retornou uma resposta vazia.")

    try:
        return json.loads(texto_resposta)
    except json.JSONDecodeError as erro:
        raise ValueError("A IA retornou uma resposta inválida. Tente novamente.") from erro
