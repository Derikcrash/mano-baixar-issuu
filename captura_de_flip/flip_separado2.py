import requests
from PIL import Image
from io import BytesIO
import cairosvg
import os


# ============================================================
# CONFIGURAÇÃO
# ============================================================

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

# Usar a maior versão encontrada
VARIANTE_JPG = 4

# Segurança: não tentar infinitamente
MAX_PAGINAS = 200

imagens_pdf = []


# ============================================================
# FUNÇÃO DE DOWNLOAD
# ============================================================

def baixar(url):

    try:

        resposta = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        if resposta.status_code == 200:
            return resposta.content

        return None

    except Exception as e:

        print(f"       [!] Erro de conexão: {e}")

        return None


# ============================================================
# INÍCIO
# ============================================================

print("=" * 60)
print("      BRASIL ENERGIA - EDIÇÃO 507")
print("=" * 60)

print()
print("[*] Usando JPG de maior resolução:")
print(f"    pageXXXX_{VARIANTE_JPG}.jpg")

print()
print("[*] Iniciando captura...")
print()


# ============================================================
# PROCESSAR PÁGINAS
# ============================================================

for pagina in range(1, MAX_PAGINAS + 1):

    num_str = f"{pagina:04d}"

    print(
        f"-> Processando página "
        f"{pagina}..."
    )


    # --------------------------------------------------------
    # JPG DE ALTA RESOLUÇÃO
    # --------------------------------------------------------

    url_fundo = (
        f"{base_url}"
        f"files/assets/common/page-html5-substrates/"
        f"page{num_str}_{VARIANTE_JPG}.jpg"
        f"{token}"
    )

    dados_fundo = baixar(url_fundo)


    # Se não encontrou o JPG, terminou a revista
    if dados_fundo is None:

        print()
        print(
            f"[!] JPG da página {pagina} não encontrado."
        )

        print(
            "[*] Considerando que chegamos ao final."
        )

        break


    # --------------------------------------------------------
    # ABRIR JPG
    # --------------------------------------------------------

    try:

        img_fundo = Image.open(
            BytesIO(dados_fundo)
        ).convert("RGBA")

    except Exception as e:

        print(
            f"   [!] Erro ao abrir JPG: {e}"
        )

        continue


    print(
        f"   [+] JPG: "
        f"{img_fundo.width}x{img_fundo.height}"
    )


    # --------------------------------------------------------
    # SVG
    # --------------------------------------------------------

    url_svg = (
        f"{base_url}"
        f"files/assets/common/page-vectorlayers/"
        f"{num_str}.svg"
        f"{token}"
    )

    dados_svg = baixar(url_svg)


    if dados_svg is not None:

        print(
            "   [+] SVG encontrado."
        )

        try:

            # Renderiza SVG
            png_bytes = cairosvg.svg2png(
                bytestring=dados_svg
            )

            img_texto = Image.open(
                BytesIO(png_bytes)
            ).convert("RGBA")


            print(
                f"   [+] SVG renderizado: "
                f"{img_texto.width}x{img_texto.height}"
            )


            # ------------------------------------------------
            # REDIMENSIONAR SVG
            # ------------------------------------------------

            if img_texto.size != img_fundo.size:

                print(
                    f"   [*] Ajustando SVG: "
                    f"{img_texto.size} -> "
                    f"{img_fundo.size}"
                )

                img_texto = img_texto.resize(
                    img_fundo.size,
                    Image.Resampling.LANCZOS
                )


            # ------------------------------------------------
            # UNIR JPG + SVG
            # ------------------------------------------------

            img_fundo = Image.alpha_composite(
                img_fundo,
                img_texto
            )

            print(
                "   [+] JPG + SVG unificados."
            )


        except Exception as e:

            print(
                f"   [!] Erro no SVG: {e}"
            )

            print(
                "   [!] Mantendo somente o JPG."
            )


    else:

        print(
            "   [i] SVG não encontrado."
        )

        print(
            "   [i] Página será usada somente com JPG."
        )


    # --------------------------------------------------------
    # ADICIONAR AO PDF
    # --------------------------------------------------------

    imagens_pdf.append(
        img_fundo.convert("RGB")
    )

    print(
        f"   [+] Página {pagina} pronta."
    )


# ============================================================
# GERAR PDF
# ============================================================

print()
print("=" * 60)


if imagens_pdf:

    nome_pdf = (
        "brasil_energia_edicao_507.pdf"
    )


    print(
        f"[*] Total de páginas: "
        f"{len(imagens_pdf)}"
    )

    print(
        "[*] Gerando PDF..."
    )


    imagens_pdf[0].save(
        nome_pdf,
        save_all=True,
        append_images=imagens_pdf[1:],
        resolution=150.0
    )


    caminho = os.path.abspath(
        nome_pdf
    )


    print()
    print("=" * 60)
    print("             PDF GERADO")
    print("=" * 60)

    print()
    print(f"Arquivo:")
    print(caminho)

    print()


else:

    print(
        "[!] Nenhuma página foi processada."
    )
