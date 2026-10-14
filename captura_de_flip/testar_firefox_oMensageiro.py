
import os
import re

PASTA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "imagens"
)

arquivo = os.path.join(PASTA, "pagina_2.svg")

with open(arquivo, "r", encoding="utf-8") as f:
    conteudo = f.read()

imagens = re.findall(
    r"<image\b[^>]*>",
    conteudo,
    re.IGNORECASE
)

for i, imagem in enumerate(imagens, 1):
    print(f"\nImagem {i}:")
    print(imagem[:1000])

print(f"\nTotal de imagens encontradas: {len(imagens)}")
