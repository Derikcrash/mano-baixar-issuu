import requests

base_url = "https://hub.gessulli.com.br/media/magazines/10/pages/{num}.webp?v=e9bd033ba63fee12"

for num in range(1, 101):
    url = base_url.format(num=num)

    r = requests.get(url)

    if r.status_code == 200:
        with open(f"pagina-{num:02d}.webp", "wb") as f:
            f.write(r.content)

        print(f"Baixada: página {num}")
    else:
        print(f"Não encontrada: página {num} — HTTP {r.status_code}")
