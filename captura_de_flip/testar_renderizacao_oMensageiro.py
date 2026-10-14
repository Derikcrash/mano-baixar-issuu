
import os
import re

PASTA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "imagens"
)

arquivo = os.path.join(PASTA, "pagina_2.svg")

with open(arquivo, "r", encoding="utf-8") as f:
    conteudo = f.read()

print("Tamanho do SVG:", len(conteudo))
print("Elementos de texto:", len(re.findall(r"<text\b", conteudo)))
print("Imagens incorporadas:", len(re.findall(r"<image\b", conteudo)))
print("Fontes incorporadas:", len(re.findall(r"@font-face", conteudo)))
print("Referências a imagens:", len(re.findall(r"data:image", conteudo)))
print("Filtros SVG:", len(re.findall(r"<filter\b", conteudo)))
