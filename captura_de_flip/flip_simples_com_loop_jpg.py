import requests

url = "https://cdn-assets.ziniopro.com/var/issues/722968/8ac3c04998b3fc4ab641dbc07e78d182/preview_image/page-{num:05d}.jpg"

for num in range(1, 150):
    r = requests.get(url.format(num=num))

    if r.status_code == 200:
        with open(f"pagina-{num:02d}.jpg", "wb") as f:
            f.write(r.content)
        print(f"Baixada: página {num}")
    else:
        print(f"Não encontrada: página {num}")
