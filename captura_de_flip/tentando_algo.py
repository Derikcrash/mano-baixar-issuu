import os
import requests

BASE = "https://api-flip.ojc.com.br/pagina"
START_ID = 564400
END_ID = 564500

TOKEN = os.getenv("OP_TOKEN")

if not TOKEN:
    raise SystemExit(
        "Defina o token primeiro:\n"
        "Linux/macOS: export OP_TOKEN='SEU_TOKEN'\n"
        "Windows PowerShell: $env:OP_TOKEN='SEU_TOKEN'"
    )

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://opopular.com.br",
    "Referer": "https://opopular.com.br/",
}

session = requests.Session()
session.headers.update(headers)

print(f"Testando IDs {START_ID} até {END_ID}...\n")

encontrados = []

for page_id in range(START_ID, END_ID + 1):
    url = f"{BASE}/pdf/{page_id}.pdf"

    try:
        response = session.head(url, timeout=10)

        # Alguns servidores não aceitam HEAD.
        if response.status_code == 405:
            response = session.get(
                url,
                headers={**headers, "Range": "bytes=0-20"},
                timeout=10,
            )

        if response.status_code == 200:
            encontrados.append(page_id)
            print(f"[OK] {page_id} -> {url}")
        elif response.status_code == 401:
            print(f"[401] {page_id} -> não autorizado")
        elif response.status_code == 404:
            print(f"[404] {page_id} -> não existe")
        else:
            print(f"[{response.status_code}] {page_id}")

    except requests.RequestException as e:
        print(f"[ERRO] {page_id}: {e}")


print("\n=== RESULTADO ===")

for page_id in encontrados:
    print(f"""
ID: {page_id}
PDF: https://api-flip.ojc.com.br/pagina/pdf/{page_id}.pdf
JPG: https://api-flip.ojc.com.br/pagina/img/alta/{page_id}.jpg
""")

print(f"Total encontrado: {len(encontrados)}")
