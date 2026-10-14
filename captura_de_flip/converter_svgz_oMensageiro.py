import os
import cairosvg

PASTA = "imagens"

for numero in range(1, 21):
    entrada = os.path.join(PASTA, f"pagina_{numero}.svgz")
    saida = os.path.join(PASTA, f"pagina_{numero}.png")

    if not os.path.isfile(entrada):
        print(f"Arquivo não encontrado: {entrada}")
        continue

    try:
        with open(entrada, "rb") as arquivo:
            conteudo = arquivo.read()

        # Se o arquivo realmente estiver compactado com gzip,
        # o CairoSVG poderá precisar receber o conteúdo descompactado.
        if conteudo[:2] == b"\x1f\x8b":
            import gzip
            conteudo = gzip.decompress(conteudo)

        # Converte o SVG para PNG em resolução ampliada
        cairosvg.svg2png(
            bytestring=conteudo,
            write_to=saida,
            scale=3
        )

        print(f"Página {numero} convertida: {saida}")

    except Exception as erro:
        print(f"Erro na página {numero}: {erro}")

print("Processo concluído!")