from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

pasta = Path(
    "/home/derik/Documentos/nano baixar_issuu.py/topview_317"
)

miniaturas = []

for n in range(1, 13):
    arquivo = pasta / f"captura_{n:04d}.webp"

    if not arquivo.exists():
        continue

    img = Image.open(arquivo).convert("RGB")
    img.thumbnail((240, 260))

    quadro = Image.new("RGB", (260, 300), "white")
    quadro.paste(img, ((260 - img.width) // 2, 25))

    draw = ImageDraw.Draw(quadro)
    draw.text((10, 5), f"Arquivo {n}", fill="black")

    miniaturas.append(quadro)

colunas = 4
linhas = (len(miniaturas) + colunas - 1) // colunas

montagem = Image.new(
    "RGB",
    (colunas * 260, linhas * 300),
    "#cccccc"
)

for i, img in enumerate(miniaturas):
    x = (i % colunas) * 260
    y = (i // colunas) * 300
    montagem.paste(img, (x, y))

saida = pasta / "contato_paginas.jpg"
montagem.save(saida, quality=90)

print(f"Montagem criada: {saida}")