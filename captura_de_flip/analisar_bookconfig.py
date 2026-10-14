import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.revide.com.br/edicoes/impressa/view/1334/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 Chrome/131.0 Safari/537.36"
}

resposta = requests.get(URL, headers=HEADERS, timeout=30)
resposta.raise_for_status()

soup = BeautifulSoup(resposta.text, "html.parser")

print("Título:", soup.title.get_text(" ", strip=True) if soup.title else "Não encontrado")
print("\n--- IFRAMEs ---")

for iframe in soup.find_all("iframe"):
    src = iframe.get("src")
    if src:
        print(urljoin(URL, src))

print("\n--- LINKS PDF ---")

for link in soup.find_all("a", href=True):
    href = urljoin(URL, link["href"])
    if ".pdf" in href.lower():
        print(href)

print("\n--- JAVASCRIPT ---")

for script in soup.find_all("script", src=True):
    print(urljoin(URL, script["src"]))

print("\n--- POSSÍVEIS CONFIGURAÇÕES DO VISUALIZADOR ---")

for termo in ["fliphtml5", "pdf", "pageCount", "totalPages", "bookConfig"]:
    if termo.lower() in resposta.text.lower():
        print(f"Encontrado no HTML: {termo}")
