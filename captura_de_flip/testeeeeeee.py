import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

BASE = "https://online.fliphtml5.com/ydgrj/Revide-1334_-CGJI/"
ARQUIVO = Path("recursos_fliphtml5.txt")
PASTA = Path("imagens_teste")
PASTA.mkdir(exist_ok=True)

sessao = requests.Session()
sessao.headers.update({"User-Agent": "Mozilla/5.0"})

vistos = set()
contador = 0

with ARQUIVO.open(encoding="utf-8") as f:
    for linha in f:
        partes = linha.rstrip("\n").split("\t", 2)
        if len(partes) != 3:
            continue

        status, tipo, url = partes

        if tipo != "image" or "/files/large/" not in url:
            continue

        if url in vistos:
            continue
        vistos.add(url)

        try:
            resposta = sessao.get(url, timeout=30)
            resposta.raise_for_status()

            img = Image.open(BytesIO(resposta.content))
            img.load()

            contador += 1
            destino = PASTA / f"imagem_{contador:03d}.webp"
            destino.write_bytes(resposta.content)

            print(
                f"{destino}: {img.size[0]}x{img.size[1]} "
                f"({len(resposta.content)} bytes)"
            )

        except Exception as e:
            print("Falha:", url, "-", e)

print(f"\nTotal de imagens verificadas: {contador}")
print("Arquivos salvos em:", PASTA.resolve())