import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter

PASTA = Path(__file__).resolve().parent.parent / "imagens"

ARQUIVO_FINAL = PASTA / "o_mensageiro_completo.pdf"

arquivos = sorted(
    PASTA.glob("pagina_*.svgz"),
    key=lambda arquivo: int(arquivo.stem.split("_")[1])
)

if not arquivos:
    print("Nenhum arquivo pagina_*.svgz encontrado na pasta imagens.")
    raise SystemExit

print(f"Encontradas {len(arquivos)} páginas.")

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=True)
    pagina = navegador.new_page()

    pdfs_temporarios = []

    for numero, arquivo in enumerate(arquivos, start=1):
        print(f"Convertendo página {numero}/{len(arquivos)}...")

        caminho_pdf = PASTA / f"temporario_{numero:03}.pdf"

        pagina.goto(
            arquivo.resolve().as_uri(),
            wait_until="load"
        )

        pagina.emulate_media(media="screen")

        pagina.pdf(
            path=str(caminho_pdf),
            width="1156px",
            height="1600px",
            print_background=True,
            margin={
                "top": "0",
                "right": "0",
                "bottom": "0",
                "left": "0"
            }
        )

        pdfs_temporarios.append(caminho_pdf)

    navegador.close()

escritor = PdfWriter()

for arquivo_pdf in pdfs_temporarios:
    escritor.append(str(arquivo_pdf))

with open(ARQUIVO_FINAL, "wb") as arquivo_saida:
    escritor.write(arquivo_saida)

escritor.close()

for arquivo_pdf in pdfs_temporarios:
    arquivo_pdf.unlink()

print("\nDownload já realizado e conversão concluída!")
print(f"PDF salvo em: {ARQUIVO_FINAL}")
print(f"Total de páginas: {len(arquivos)}")