import os

PASTA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "imagens"
)

arquivo_entrada = os.path.join(PASTA, "pagina_2.svgz")
arquivo_saida = os.path.join(PASTA, "pagina_2.svg")

with open(arquivo_entrada, "rb") as entrada:
    conteudo = entrada.read()

with open(arquivo_saida, "wb") as saida:
    saida.write(conteudo)

print("Arquivo salvo:", arquivo_saida)