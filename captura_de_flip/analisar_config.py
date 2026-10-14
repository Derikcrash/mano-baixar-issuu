import requests
import re
import json
from pathlib import Path

BASE = "https://online.fliphtml5.com/ydgrj/Revide-1334_-CGJI/"
CONFIG_URL = BASE + "javascript/config.js?1791539957"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
    "Referer": BASE,
}

res = requests.get(CONFIG_URL, headers=HEADERS, timeout=30)

print("Status HTTP:", res.status_code)
print("Content-Type:", res.headers.get("Content-Type"))
res.raise_for_status()

texto = res.text
Path("revide_config.js").write_text(texto, encoding="utf-8")

print("Tamanho:", len(texto), "caracteres")
print("\n=== INÍCIO DA CONFIGURAÇÃO ===")
print(texto[:3500])

print("\n=== POSSÍVEIS DADOS DAS PÁGINAS ===")

termos = [
    "pageCount", "totalPages", "pageNum", "pagecount",
    "fliphtml5_pages", "files", "large", "medium",
    "thumb", "bookConfig", "page", "pdf"
]

for termo in termos:
    ocorrencias = list(re.finditer(re.escape(termo), texto, re.I))
    if ocorrencias:
        print(f"\n[{termo}] - {len(ocorrencias)} ocorrência(s)")
        for m in ocorrencias[:3]:
            inicio = max(0, m.start() - 180)
            fim = min(len(texto), m.end() + 350)
            print(texto[inicio:fim].replace("\n", " ")[:600])

print("\n=== URLS ENCONTRADAS ===")
urls = list(dict.fromkeys(re.findall(
    r'https?://[^"\'\s<>]+|//[^"\'\s<>]+',
    texto
)))

for url in urls[:40]:
    print(url)

print("\nArquivo salvo em: revide_config.js")