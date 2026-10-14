import requests
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# ===== CONFIGURAÇÃO =====
DATA = "2026-10-10"  # Altere para 2026-10-08, 2026-10-09 etc.
TOTAL_PAGINAS = 50
PASTA = Path("edicoes")
# ========================

ano, mes, dia = DATA.split("-")

url = (
    "https://larepublica.cronosmedia.glr.pe/"
    f"printed/{ano}/{mes}/{dia}/lima/pages/"
    "{num:02d}.jpeg"
)
#printed/2026/10/12/lima/pages/01.jpeg
PASTA.mkdir(exist_ok=True)
pdf_saida = PASTA / f"La_Republica_Lima_{DATA}.pdf"


def baixar_pagina(num):
    try:
        resposta = requests.get(
            url.format(num=num),
            timeout=25
        )

        if resposta.status_code != 200:
            print(f"Página {num}: não encontrada")
            return num, None

        imagem = Image.open(BytesIO(resposta.content))
        imagem.load()

        if imagem.format not in ("JPEG", "PNG", "WEBP"):
            print(f"Página {num}: formato inválido")
            return num, None

        imagem = imagem.convert("RGB")
        print(f"Página {num}: baixada")

        return num, imagem

    except Exception as erro:
        print(f"Página {num}: erro - {erro}")
        return num, None


paginas = []

with ThreadPoolExecutor(max_workers=5) as executor:
    resultados = executor.map(
        baixar_pagina,
        range(1, TOTAL_PAGINAS + 1)
    )

    paginas = [
        (num, imagem)
        for num, imagem in resultados
        if imagem is not None
    ]

# Mantém a ordem correta das páginas
paginas.sort(key=lambda item: item[0])

imagens = [imagem for _, imagem in paginas]

if imagens:
    imagens[0].save(
        pdf_saida,
        save_all=True,
        append_images=imagens[1:],
        resolution=150
    )

    print(f"\nPDF criado: {pdf_saida}")
    print(f"Total de páginas: {len(imagens)}")

    for imagem in imagens:
        imagem.close()
else:
    print("Nenhuma página foi encontrada.")