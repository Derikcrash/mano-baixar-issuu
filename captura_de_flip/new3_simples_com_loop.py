import requests

url = "https://cdnne.directreader.it/issues/pub_5a1d6930cf9f5/5000-07-21/8ac048f/pages/medium/002.jpg-{num:05d}.jpg"

for num in range(1, 101):
    r = requests.get(url.format(num=num))

    if r.status_code == 200:
        with open(f"pagina-{num:02d}.jpg", "wb") as f:
            f.write(r.content)
        print(f"Baixada: página {num}")
    else:
        print(f"Não encontrada: página {num}")