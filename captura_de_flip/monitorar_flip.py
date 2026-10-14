import asyncio
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

URL = "https://online.fliphtml5.com/ydgrj/Revide-1334_-CGJI/"

async def main():
    recursos = {}
    erros = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            viewport={"width": 1440, "height": 1000}
        )

        def registrar_request(req):
            recursos[req.url] = {
                "metodo": req.method,
                "tipo": req.resource_type,
                "status": None,
            }

        def registrar_response(res):
            item = recursos.setdefault(
                res.url,
                {
                    "metodo": res.request.method,
                    "tipo": res.request.resource_type,
                    "status": None,
                },
            )
            item["status"] = res.status

        page.on("request", registrar_request)
        page.on("response", registrar_response)
        page.on("requestfailed", lambda req: erros.append(
            f"{req.url} | {req.failure}"
        ))

        print("Abrindo a edição...")
        await page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000,
        )
        await page.wait_for_timeout(8000)

        print("Título:", await page.title())

        # Tenta avançar algumas páginas usando o teclado.
        for numero in range(1, 5):
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(2000)
            print(f"Página explorada: {numero + 1}")

        linhas = []
        for url, info in sorted(recursos.items()):
            tipo = info["tipo"]
            caminho = urlparse(url).path.lower()

            relevante = (
                tipo in ("image", "media")
                or caminho.endswith((".jpg", ".jpeg", ".png",
                                     ".webp", ".svg", ".json",
                                     ".pdf", ".bin"))
                or "config" in caminho
                or "page" in caminho
            )

            if relevante:
                linhas.append(
                    f'{info["status"]}\t{tipo}\t{url}'
                )

        Path("recursos_fliphtml5.txt").write_text(
            "\n".join(linhas),
            encoding="utf-8",
        )

        Path("erros_fliphtml5.txt").write_text(
            "\n".join(erros),
            encoding="utf-8",
        )

        print("\nRecursos relevantes:", len(linhas))
        print("Lista salva em recursos_fliphtml5.txt")
        print("Falhas salvas em erros_fliphtml5.txt")

        for linha in linhas[:40]:
            print(linha)

        await browser.close()

asyncio.run(main())
