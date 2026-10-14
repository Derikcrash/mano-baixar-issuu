import requests

base_url = (
    "https://brasilenergia.z21.web.core.windows.net/"
    "flip/1096/"
    "7cbca74f12a5409ba8c71b3d2bdbf8b8/"
    "Bia507/"
)

token = "?uni=c6a880e7e76aa12fa1b835bed6b93ac6"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def testar(url):
    try:
        r = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if r.status_code != 200:
            return f"{r.status_code}"

        content_type = r.headers.get("Content-Type", "")

        # JPEG
        if "image" in content_type:
            try:
                from PIL import Image
                from io import BytesIO

                img = Image.open(BytesIO(r.content))

                return f"OK - {img.size[0]}x{img.size[1]}"

            except:
                return f"OK - {len(r.content)} bytes"

        return f"OK - {content_type}"

    except Exception as e:
        return f"ERRO - {e}"


for pagina in range(1, 6):

    num = f"{pagina:04d}"

    print()
    print("=" * 50)
    print(f"PÁGINA {pagina}")
    print("=" * 50)

    # Testa JPGs
    for variante in range(1, 6):

        url = (
            f"{base_url}"
            f"files/assets/common/page-html5-substrates/"
            f"page{num}_{variante}.jpg"
            f"{token}"
        )

        resultado = testar(url)

        print(
            f"JPG _{variante}: {resultado}"
        )

    # Testa SVG
    url_svg = (
        f"{base_url}"
        f"files/assets/common/page-vectorlayers/"
        f"{num}.svg"
        f"{token}"
    )

    resultado_svg = testar(url_svg)

    print(
        f"SVG: {resultado_svg}"
    )
