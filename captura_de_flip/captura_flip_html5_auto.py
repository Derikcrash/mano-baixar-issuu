
import requests
import re
import os
from urllib.parse import urljoin

url = "https://online.fliphtml5.com/ydgrj/Revide-1334_-CGJI/"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/154.0.0.0 Safari/537.36"
}

sessao = requests.Session()

resposta = sessao.get(
    url,
    headers=headers,
    timeout=30
)

print("Status HTTP:", resposta.status_code)
print("URL final:", resposta.url)
print("Tamanho do HTML:", len(resposta.text))

html = resposta.text

os.makedirs("diagnostico_rev ide".replace(" ", ""), exist_ok=True)

with open("diagnostico_rev ide.html".replace(" ", ""), "w", encoding="utf-8") as arquivo:
    arquivo.write(html)

print("\n--- REFERÊNCIAS NO HTML ---")

padroes = [
    r'<script[^>]+src=["\']([^"\']+)',
    r'[^"\']*files/large/[^"\']*',
    r'[^"\']*files/assets/[^"\']*',
    r'[^"\']*config[^"\']*',
    r'[^"\']*pageCount[^"\']*',
    r'[^"\']*d42605df9119f3cf29a5bf303ac384bf[^"\']*',
    r'[^"\']*f18e25138880543d0205c39be61c61af[^"\']*'
]

for padrao in padroes:
    encontrados = re.findall(padrao, html, re.IGNORECASE)

    for item in encontrados[:20]:
        print(item)

print("\n--- INÍCIO DO HTML ---")
print(html[:1500])

print("\nHTML salvo em diagnostico_rev ide.html")
