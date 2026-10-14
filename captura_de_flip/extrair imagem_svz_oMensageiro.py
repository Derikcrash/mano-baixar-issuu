
import os
import re
import base64
from PIL import Image
from io import BytesIO

PASTA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "imagens"
)

arquivo = os.path.join(PASTA, "pagina_2.svg")

with open(arquivo, "r", encoding="utf-8") as f:
    conteudo = f.read()

resultado = re.search(
    r'data:image/jpeg;base64,([^"]+)',
    conteudo
)

if resultado:
    dados = base64.b64decode(resultado.group(1))

    caminho = os.path.join(PASTA, "imagem_extraida.jpg")

    with open(caminho, "wb") as f:
        f.write(dados)

    imagem = Image.open(BytesIO(dados))

    print("Imagem extraída:", caminho)
    print("Resolução:", imagem.size)
else:
    print("Imagem JPEG não encontrada.")
