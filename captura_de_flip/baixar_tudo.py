import asyncio
from pathlib import Path
from io import BytesIO
import requests
from PIL import Image
from playwright.async_api import async_playwright

URL = "https://online.fliphtml5.com/ydgrj/Revide-1334_-CGJI/"
PASTA = Path("revide_paginas")
PASTA.mkdir(exist_ok=True)

async def main():
    urls = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        async def registrar(response):
            u = response.url
            if ("/files/large/" in u and
                u.lower().split("?")[0].endswith((".webp", ".jpg", ".jpeg", ".png"))):
                urls.add(u)

        page.on("response", registrar)

        print("Abrindo revista...")
        await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(8000)

        # Tenta avançar automaticamente pelas páginas.
        for i in range(34):
            print(f"Explorando página {i + 1}/34...")
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(1200)

        await page.wait_for_timeout(3000)
        await browser.close()

    print(f"\nImagens encontradas: {len(urls)}")

    sessao = requests.Session()
    sessao.headers["User-Agent"] = "Mozilla/5.0"
    imagens = []

    for i, url in enumerate(sorted(urls), 1):
        try:
            r = sessao.get(url, timeout=60)
            r.raise_for_status()
            img = Image.open(BytesIO(r.content)).convert("RGB")
            img.save(PASTA / f"pagina_{i:03d}.jpg", quality=95)
            imagens.append((url, img.copy()))
            print(f"Baixada {i}/{len(urls)}")
        except Exception as e:
            print(f"Falha: {url} — {e}")

    if imagens:
        # Os nomes das imagens são hashes, portanto a ordem alfabética
        # não garante a ordem das páginas da revista.
        imagens[0][1].save(
            "revide_1334.pdf",
            save_all=True,
            append_images=[x[1] for x in imagens[1:]],
            resolution=150
        )
        print(f"\nPDF criado com {len(imagens)} imagens: revide_1334.pdf")
    else:
        print("Nenhuma imagem encontrada.")

asyncio.run(main())
