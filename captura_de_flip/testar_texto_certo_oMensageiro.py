
import os

PASTA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "imagens"
)

for nome in ["pagina_1.svgz", "pagina_2.svgz", "pagina_2.svg"]:
    caminho = os.path.join(PASTA, nome)

    if os.path.exists(caminho):
        tamanho = os.path.getsize(caminho)

        with open(caminho, "rb") as arquivo:
            inicio = arquivo.read(20)

        print(f"\nArquivo: {nome}")
        print(f"Tamanho: {tamanho:,} bytes")
        print(f"Início do conteúdo: {inicio}")
    else:
        print(f"\nArquivo não encontrado: {nome}")
