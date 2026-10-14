import asyncio
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

EDICAO_URL = (
    "https://www.revide.com.br/"
    "edicoes/impressa/view/1334/"
)

PASTA = Path("revide_1334")
PASTA.mkdir(parents=True, exist_ok=True)

MAX_PAGINAS = 180
ESPERA = 1.0

# URL -> metadados da imagem capturada
capturadas = {}
tarefas = []


async def salvar_resposta(response):
    try:
        url = response.url
        parsed = urlparse(url)

        # Restringe a captura aos recursos do FlipHTML5.
        if "fliphtml5.com" not in (parsed.hostname or ""):
            return

        headers = await response.all_headers()
        tipo = headers.get("content-type", "").lower()

        if not tipo.startswith("image/"):
            return

        if response.status != 200:
            return

        conteudo = await response.body()

        # Ignora respostas vazias ou excessivamente pequenas.
        if len(conteudo) < 1000:
            return

        digest = hashlib.sha256(conteudo).hexdigest()

        extensoes = {
            "image/webp": ".webp",
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/avif": ".avif",
        }

        extensao = extensoes.get(tipo.split(";")[0], ".img")
        nome = f"{digest}{extensao}"
        destino = PASTA / nome

        if not destino.exists():
            destino.write_bytes(conteudo)

        capturadas[url] = {
            "arquivo": nome,
            "bytes": len(conteudo),
            "sha256": digest,
        }

        print(f"[OK] {nome} ({len(conteudo)} bytes)")

    except Exception as erro:
        print(f"[AVISO] Falha ao capturar resposta: {erro}")


async def main():
    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=False)

        contexto = await navegador.new_context(
            viewport={"width": 1440, "height": 1000}
        )

        pagina = await contexto.new_page()

        def ao_receber_resposta(response):
            tarefa = asyncio.create_task(
                salvar_resposta(response)
            )
            tarefas.append(tarefa)

        pagina.on("response", ao_receber_resposta)

        print("Abrindo a edição da Revide...")
        await pagina.goto(
            EDICAO_URL,
            wait_until="domcontentloaded",
            timeout=90000,
        )

        await pagina.wait_for_timeout(6000)

        print("\nFrames encontrados:")
        for frame in pagina.frames:
            print(" -", frame.url)

        print("\nAguardando o carregamento inicial...")
        await pagina.wait_for_timeout(5000)

        for numero in range(MAX_PAGINAS):
            # Tenta avançar no visualizador.
            try:
                await pagina.keyboard.press("ArrowRight")
            except Exception:
                pass

            await pagina.wait_for_timeout(
                int(ESPERA * 1000)
            )

            if (numero + 1) % 10 == 0:
                print(
                    f"Avanço {numero + 1}/"
                    f"{MAX_PAGINAS} | "
                    f"{len(capturadas)} URLs capturadas"
                )

        # Aguarda as últimas respostas de imagem.
        if tarefas:
            await asyncio.gather(
                *tarefas, return_exceptions=True
            )

        await navegador.close()

    inventario = {
        "edicao": EDICAO_URL,
        "imagens": capturadas,
    }

    (PASTA / "inventario.json").write_text(
        json.dumps(
            inventario,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\nFinalizado.")
    print(f"URLs capturadas: {len(capturadas)}")
    print(f"Arquivos salvos em: {PASTA.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())