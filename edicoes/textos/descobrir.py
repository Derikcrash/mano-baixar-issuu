import requests
import os
from pathlib import Path

BASE = "https://api-flip.ojc.com.br/pagina/img/alta"

# Faixa inicial para investigar
START_ID = 564400
END_ID = 564500

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:157.0) Gecko/20100101 Firefox/157.0",
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://opopular.com.br",
    "Referer": "https://opopular.com.br/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}

session = requests.Session()
session.headers.update(headers)

pasta = Path("paginas")
pasta.mkdir(exist_ok=True)

encontrados = []

for page_id in range(START_ID, END_ID + 1):

    url = f"{BASE}/{page_id}.jpg"

    try:
        r = session.get(url, timeout=15)

        if r.status_code == 200 and r.content:
            tamanho = len(r.content)

            print(f"[OK] {page_id} | {tamanho:,} bytes")

            arquivo = pasta / f"{page_id}.jpg"
            arquivo.write_bytes(r.content)

            encontrados.append(page_id)

        elif r.status_code == 401:
            print(f"[401] {page_id} | não autorizado")

        elif r.status_code == 404:
            print(f"[404] {page_id} | não encontrado")

        else:
            print(f"[{r.status_code}] {page_id}")

    except requests.RequestException as e:
        print(f"[ERRO] {page_id}: {e}")


print()
print("=" * 50)
print("PÁGINAS ENCONTRADAS")
print("=" * 50)

for page_id in encontrados:
    print(page_id)

print()
print(f"Total: {len(encontrados)}")
print(f"Arquivos salvos em: {pasta.resolve()}")
