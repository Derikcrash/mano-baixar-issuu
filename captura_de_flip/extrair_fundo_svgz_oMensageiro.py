import re
import base64
from pathlib import Path

entrada = Path("imagens/pagina_2.svgz")
saida = Path("imagens/pagina_2_fundo.jpg")

svg = entrada.read_text(encoding="utf-8")

# Localiza a imagem JPEG incorporada no SVG
resultado = re.search(
    r'xlink:href="data:image/jpeg;base64,([^"]+)"',
    svg
)

if not resultado:
    raise RuntimeError("Imagem JPEG incorporada não encontrada.")

dados = base64.b64decode(resultado.group(1))
saida.write_bytes(dados)

print(f"Imagem extraída: {saida}")
print(f"Tamanho: {len(dados):,} bytes")
