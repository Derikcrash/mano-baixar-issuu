import asyncio
import json
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from io import BytesIO
from playwright.async_api import async_playwright


URL = "https://online.fliphtml5.com/topview/tfxa/"
TOTAL_PAGINAS = 136
PASTA = Path("topview_317")
PASTA.mkdir(exist_ok=True)

# Mantém a ordem em que cada URL foi descoberta
imagens = {}


def registrar_url(url):
    """Registra somente imagens grandes da edição."""
    parsed = urlparse(url)

    if (
        parsed.hostname == "online.fliphtml5.com"
        and "/topview/tfxa/files/large/" in parsed.path
        and parsed.path.lower().endswith(".webp")
    ):
        imagens.setdefault(url, len(imagens) + 1)


async def main():
    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=False)
        pagina = await navegador.new_page(
            viewport={"width": 1440, "height": 1000}
        )

        pagina.on(
            "request",
            lambda req: registrar_url(req.url)
        )

        print("Abrindo a revista...")
        await pagina.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=90000
        )

        await pagina.wait_for_timeout(10000)

        # Inspeciona os objetos disponibilizados pelo visualizador
        config = await pagina.evaluate("""() => {
            function resumo(obj) {
                if (!obj || typeof obj !== "object") return obj;
                return {
                    keys: Object.keys(obj).slice(0, 100),
                    totalPageCount: obj.totalPageCount,
                    pageCount: obj.pageCount,
                    largePath: obj.largePath,
                    normalPath: obj.normalPath,
                    pagesCount: Array.isArray(obj.pages)
                        ? obj.pages.length : null
                };
            }

            return {
                meta: window.htmlConfig?.meta || null,
                bookConfig: resumo(window.bookConfig),
                readerConfig: resumo(window.readerConfig)
            };
        }""")

        (PASTA / "config_runtime.json").write_text(
            json.dumps(config, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        print("Configuração do visualizador:")
        print(json.dumps(config, indent=2, ensure_ascii=False)[:5000])

        print(f"\nImagens iniciais: {len(imagens)}")

        # Tenta percorrer a publicação.
        # O visualizador pode responder às setas ou PageDown.
        sem_novas = 0
        anterior = len(imagens)

        for passo in range(TOTAL_PAGINAS):
            await pagina.keyboard.press("ArrowRight")
            await pagina.wait_for_timeout(700)

            if len(imagens) == anterior:
                sem_novas += 1
            else:
                sem_novas = 0
                anterior = len(imagens)

            if (passo + 1) % 10 == 0:
                print(
                    f"Avanço {passo + 1}/{TOTAL_PAGINAS}: "
                    f"{len(imagens)} imagens"
                )

            # Se não houver atividade, tenta outra tecla
            if sem_novas == 10:
                await pagina.keyboard.press("PageDown")
                await pagina.wait_for_timeout(1200)
                sem_novas = 0
                anterior = len(imagens)

        await navegador.close()

    # Inventário de URLs
    lista = list(imagens.keys())

    (PASTA / "urls.json").write_text(
        json.dumps(lista, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"\nURLs únicas encontradas: {len(lista)}")

    if not lista:
        print("Nenhuma imagem encontrada. Verifique config_runtime.json.")
        return

    # Baixa as imagens na ordem em que foram descobertas
    sessao = requests.Session()
    sessao.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Referer": URL
    })

    paginas_pdf = []

    for indice, url in enumerate(lista, start=1):
        destino = PASTA / f"captura_{indice:04d}.webp"

        try:
            resposta = sessao.get(url, timeout=40)
            resposta.raise_for_status()

            imagem = Image.open(
                BytesIO(resposta.content)
            )
            imagem.verify()

            destino.write_bytes(resposta.content)
            print(f"[OK] {destino.name}")

        except Exception as erro:
            print(f"[ERRO] {indice}: {erro}")

    print("\nCaptura encerrada.")
    print("Pasta:", PASTA.resolve())
    print("Confira urls.json e config_runtime.json.")
    print(
        "Importante: a ordem de descoberta das URLs não garante "
        "a ordem original das páginas."
    )


if __name__ == "__main__":
    asyncio.run(main())