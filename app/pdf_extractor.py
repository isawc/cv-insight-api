import io

import PyPDF2


def extrair_texto_pdf(arquivo_bytes: bytes) -> str:
    arquivo = io.BytesIO(arquivo_bytes)
    leitor = PyPDF2.PdfReader(arquivo)

    # PyPDF2 não extrai texto de PDFs escaneados como imagem.
    texto = "\n".join(
        pagina.extract_text() or ""
        for pagina in leitor.pages
    ).strip()

    if not texto:
        raise ValueError(
            "Não foi possível extrair texto do PDF. "
            "O arquivo pode estar vazio, protegido ou escaneado como imagem."
        )

    return texto
