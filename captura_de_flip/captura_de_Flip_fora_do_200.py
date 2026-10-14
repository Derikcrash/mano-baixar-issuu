import requests

url = "https://cdnne.directreader.it/issues/pub_5a1d6930cf9f5/5000-07-21/8ac048f/pages/medium/{num:03d}.jpg"

for num in range(250, 400 ):
    r = requests.get(url.format(num=num))

    if r.status_code == 200:
        with open(f"pagina-{num:03d}.jpg", "wb") as f:
            f.write(r.content)
        print(f"Baixada: página {num}")
    else:
        print(f"Não encontrada: página {num} — HTTP {r.status_code}")
