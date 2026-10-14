from pathlib import Path
import re

arquivo = Path("imagens/pagina_2.svgz")
svg = arquivo.read_text(encoding="utf-8")

print("=== DIAGNÓSTICO DO SVG ===")
print("ViewBox:", re.search(r'viewBox="([^"]+)"', svg).group(1))
print("Elementos <text>:", len(re.findall(r'<text(?:\s|>)', svg)))
print("Elementos <tspan>:", len(re.findall(r'<tspan(?:\s|>)', svg)))
print("Elementos <path>:", len(re.findall(r'<path(?:\s|>)', svg)))
print("Transformações:", len(re.findall(r'\btransform=', svg)))
print("Fontes incorporadas:", svg.count("data:application/font-woff"))

print("\n=== PRIMEIROS ELEMENTOS DE TEXTO ===")
for elemento in re.findall(r'<text\b[^>]*>', svg)[:10]:
    print(elemento[:400])