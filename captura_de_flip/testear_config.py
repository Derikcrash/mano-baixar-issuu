
import os
import requests
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright

url = "https://online.fliphtml5.com/ydgrj/Revide-1334_-CGJI/"
base = url.rstrip("/") + "/"

os.makedirs("revide_1334", exist_ok=True)

print("Abrindo a edição no navegador...")

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=True)
    pagina = navegador.new_page()

    pagina.goto(url, wait_until="domcontentloaded", timeout=60000)

    try:
        print("Aguardando o carregamento do módulo...")

        pagina.wait_for_function(
            """() => {
                const m = window.Module;

                return window.htmlConfig &&
                       window.htmlConfig.fliphtml5_pages &&
                       m &&
                       m.calledRun === true &&
                       typeof m._DeString === "function" &&
                       typeof window.allocateUTF8 === "function" &&
                       typeof window.UTF8ToString === "function";
            }""",
            timeout=60000
        )

        print("Decodificando a lista de páginas...")

        arquivos = pagina.evaluate("""() => {
            const criptografado =
                window.htmlConfig.fliphtml5_pages;

            const ponteiro =
                window.allocateUTF8(criptografado);

            const resultado =
                window.Module._DeString(ponteiro);

            const texto =
                window.UTF8ToString(resultado);

            const fim = texto.lastIndexOf("]");

            if (fim === -1) {
                throw new Error(
                    "A lista de páginas não foi decodificada corretamente."
                );
            }

            const paginas = JSON.parse(
                texto.slice(0, fim + 1)
            );

            return paginas
                .map(p => p.n && p.n[0])
                .filter(Boolean);
        }""")

    except Exception as erro:
        print("Não foi possível decodificar as páginas.")
        print("Erro:", erro)
        navegador.close()
        raise SystemExit

    navegador.close()

print("Páginas encontradas:", len(arquivos))

if not arquivos:
    print("Nenhuma página foi identificada.")
    raise SystemExit

sessao = requests.Session()
sessao.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": url
})

imagens_pdf = []

for i, arquivo in enumerate(arquivos, start=1):
    caminho_url = arquivo.replace("\\", "").replace("../", "")

    if caminho_url.startswith("http"):
        imagem_url = caminho_url
    elif caminho_url.startswith("files/"):
        imagem_url = base + caminho_url
    else:
        imagem_url = base + "files/large/" + caminho_url

    try:
        resposta = sessao.get(imagem_url, timeout=40)
        resposta.raise_for_status()

        imagem = Image.open(
            BytesIO(resposta.content)
        ).convert("RGB")

        caminho_imagem = f"revide_1334/pagina_{i:02d}.jpg"
        imagem.save(caminho_imagem, quality=95)

        imagens_pdf.append(imagem)

        print(f"[{i}/{len(arquivos)}] Página baixada")

    except Exception as erro:
        print(f"[{i}/{len(arquivos)}] Erro: {erro}")

if imagens_pdf:
    nome_pdf = "revide_1334.pdf"

    imagens_pdf[0].save(
        nome_pdf,
        save_all=True,
        append_images=imagens_pdf[1:],
        resolution=150
    )

    print("\nPDF criado:", os.path.abspath(nome_pdf))
    print("Páginas incluídas:", len(imagens_pdf))
else:
    print("Nenhuma imagem foi baixada.")
