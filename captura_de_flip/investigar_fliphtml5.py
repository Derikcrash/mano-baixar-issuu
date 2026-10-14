import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://online.fliphtml5.com/ydgrj/Revide-1334_-CGJI/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}

res = requests.get(URL, headers=HEADERS, timeout=30)
print("Status HTTP:", res.status_code)
print("URL final:", res.url)
res.raise_for_status()

html = res.text

with open("revide_fliphtml5.html", "w", encoding="utf-8") as f:
    f.write(html)

soup = BeautifulSoup(html, "html.parser")

print("\n=== TÍTULO ===")
print(soup.title.get_text(" ", strip=True) if soup.title else "Sem título")

print("\n=== SCRIPTS ===")
for tag in soup.find_all("script"):
    src = tag.get("src")
    if src:
        print(urljoin(res.url, src))

print("\n=== RECURSOS RELACIONADOS AO LIVRO ===")
padroes = [
    r'https?://[^"\']+',
    r'[^"\']*bookConfig[^"\']*',
    r'[^"\']*pageCount[^"\']*',
    r'[^"\']*totalPages[^"\']*',
    r'[^"\']*files/[^"\']*',
    r'[^"\']*config[^"\']*\.js[^"\']*',
    r'[^"\']*\.json(?:\?[^"\']*)?',
]

vistos = set()

for padrao in padroes:
    for achado in re.findall(padrao, html, re.IGNORECASE):
        achado = achado.strip()
        if achado not in vistos:
            vistos.add(achado)
            print(achado[:500])

print("\nHTML salvo em: revide_fliphtml5.html")