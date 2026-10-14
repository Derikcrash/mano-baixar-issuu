from pathlib import Path
from PIL import Image
import re

BASE = Path("/home/derik/Documentos/nano baixar_issuu.py")
ORIGEM = BASE / "topview_317"
SAIDA = BASE / "topview_317_corrigida.pdf"

def numero(arquivo):
    m = re.search(r"captura_(\d+)\.webp$", arquivo.name)
    return int(m.group(1)) if m else None

arquivos = sorted(
    [p for p in ORIGEM.glob("captura_*.webp") if numero(p)],
    key=numero
)

if not arquivos:
    raise SystemExit(f"Nenhuma imagem encontrada em {ORIGEM}")

# Preserva as três primeiras páginas e inverte os pares seguintes.
ordenados = arquivos[:3]
resto = arquivos[3:]

for i in range(0, len(resto), 2):
    par = resto[i:i + 2]
    ordenados.extend(par[::-1])

imagens = []

for arquivo in ordenados:
    with Image.open(arquivo) as img:
        imagens.append(img.convert("RGB").copy())
    print(f"Adicionada: {arquivo.name}")

if imagens:
    imagens[0].save(
        SAIDA,
        "PDF",
        save_all=True,
        append_images=imagens[1:],
        resolution=150
    )

    for img in imagens:
        img.close()

    print(f"\nPDF criado: {SAIDA}")
    print(f"Total de páginas: {len(ordenados)}")
