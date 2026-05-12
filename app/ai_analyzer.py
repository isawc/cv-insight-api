import json

import anthropic

from app.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS

cliente = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


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

    resposta = cliente.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    texto_resposta = resposta.content[0].text

    try:
        return json.loads(texto_resposta)
    except json.JSONDecodeError as erro:
        raise ValueError("A IA retornou uma resposta inválida. Tente novamente.") from erro
