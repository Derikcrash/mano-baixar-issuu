import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "https://online.fliphtml5.com/ydgrj/Revide-1334_-CGJI/"
ARQUIVO = Path("recursos_paginas.txt")


async def main():
    recursos = []
    vistos = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        def registrar(response):
            url = response.url
            if (
                response.status == 200
                and ".webp" in url.lower()
                and "/files/large/" in url
                and url not in vistos
            ):
                vistos.add(url)
                recursos.append(url)
                ARQUIVO.write_text(
                    "\n".join(recursos) + "\n",
                    encoding="utf-8",
                )
                print(f"Imagem distinta: {len(recursos)}")

        page.on("response", registrar)

        await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(5000)

        print("\nAvance página por página no visualizador.")
        print("A lista será salva automaticamente.")
        print("Feche o navegador para encerrar.")

        try:
            while not page.is_closed():
                await page.wait_for_timeout(500)
        finally:
            if not page.is_closed():
                await browser.close()

asyncio.run(main())
