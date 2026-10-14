import os
import re
import html
import requests
import cairosvg

from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


BASE = "https://svg.issuu.com/260922150634-e3b3809f37708e2e813eb4ec6c426bd0"
VERSAO = "1790089636135"

PASTA = "issuu_paginas"
PDF_FINAL = "jornal_issuu_6_paginas.pdf"

os.makedirs(PASTA, exist_ok=True)


# ---------------------------------------------------------
# FONTES
# ---------------------------------------------------------

def configurar_fontes():
    fontes = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVu"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVu-Bold"),
    ]

    for caminho, nome in fontes:
        if os.path.exists(caminho):
            pdfmetrics.registerFont(TTFont(nome, caminho))

    if "DejaVu" in pdfmetrics.getRegisteredFontNames():
        return "DejaVu", "DejaVu-Bold"

    return "Helvetica", "Helvetica-Bold"


FONTE_NORMAL, FONTE_NEGRITO = configurar_fontes()


# ---------------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------------

def baixar(url, arquivo):
    print(f"Baixando: {url}")

    resposta = requests.get(
        url,
        timeout=60,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    resposta.raise_for_status()

    with open(arquivo, "wb") as f:
        f.write(resposta.content)

    print(f"OK: {arquivo}")

    return resposta.content


# ---------------------------------------------------------
# EXTRAI TAMANHO DO SVG
# ---------------------------------------------------------

# ---------------------------------------------------------
# EXTRAI TAMANHO DO SVG (CORRIGIDO)
# ---------------------------------------------------------

def descobrir_tamanho_svg(conteudo):
    texto = conteudo.decode("utf-8", errors="ignore")

    # Busca a largura e a altura de forma independente dentro da tag <svg>
    match_width = re.search(r'<svg[^>]*width=["\']([\d.]+)', texto, re.IGNORECASE)
    match_height = re.search(r'<svg[^>]*height=["\']([\d.]+)', texto, re.IGNORECASE)

    if match_width and match_height:
        largura = float(match_width.group(1))
        altura = float(match_height.group(1))
        return largura, altura

    # Fallback para o viewBox caso não ache width/height diretos
    match_viewbox = re.search(r'viewBox=["\']([^"\']+)["\']', texto, re.IGNORECASE)

    if match_viewbox:
        valores = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', match_viewbox.group(1))

        if len(valores) >= 4:
            largura = float(valores[2])
            altura = float(valores[3])
            return largura, altura

    # fallback final
    return 1000, 1414


# ---------------------------------------------------------
# CONVERTE SVG PARA PNG
# ---------------------------------------------------------

def converter_svg_para_png(svg_arquivo, png_arquivo):
    try:
        cairosvg.svg2png(
            url=svg_arquivo,
            write_to=png_arquivo,
            output_width=1600
        )

        return True

    except Exception as e:
        print(f"AVISO: não foi possível converter SVG: {e}")
        return False


# ---------------------------------------------------------
# EXTRAI POSIÇÃO DO STYLE
# ---------------------------------------------------------

def pegar_numero(style, nome):
    match = re.search(
        rf"{nome}\s*:\s*([-+]?\d+(?:\.\d+)?)%",
        style
    )

    if match:
        return float(match.group(1))

    return 0


# ---------------------------------------------------------
# LIMPA TEXTO
# ---------------------------------------------------------

def limpar_texto(texto):
    texto = html.unescape(texto)

    texto = texto.replace("\xa0", " ")

    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


# ---------------------------------------------------------
# EXTRAI BLOCOS A11Y
# ---------------------------------------------------------

def extrair_blocos(html_bytes):
    texto_html = html_bytes.decode(
        "utf-8",
        errors="replace"
    )

    # IMPORTANTE:
    # usamos html.parser e NÃO XML.
    # Isso permite lidar com os <img> quebrados do Issuu.

    soup = BeautifulSoup(
        texto_html,
        "html.parser"
    )

    blocos = []

    for elemento in soup.select(".a11y-block"):

        # Imagens não possuem texto.
        if elemento.name == "img":
            continue

        texto = limpar_texto(
            elemento.get_text(" ", strip=True)
        )

        if not texto:
            continue

        style = elemento.get("style", "")

        left = pegar_numero(style, "left")
        top = pegar_numero(style, "top")
        width = pegar_numero(style, "width")
        height = pegar_numero(style, "height")

        classe = elemento.get("class", [])

        eh_titulo = (
            elemento.name in ["h1", "h2", "h3", "h4"]
            or "a11y-heading" in classe
        )

        blocos.append({
            "texto": texto,
            "left": left,
            "top": top,
            "width": width,
            "height": height,
            "titulo": eh_titulo
        })

    return blocos


# ---------------------------------------------------------
# TAMANHO DA FONTE
# ---------------------------------------------------------

def calcular_fonte(bloco, altura_pagina):

    altura_percentual = bloco["height"]

    if altura_percentual <= 0:
        return 8

    tamanho = (
        altura_percentual / 100
    ) * altura_pagina

    if bloco["titulo"]:
        tamanho *= 0.85
    else:
        tamanho *= 0.70

    tamanho = max(5, min(tamanho, 40))

    return tamanho


# ---------------------------------------------------------
# ESCREVE TEXTO NO PDF
# ---------------------------------------------------------

def desenhar_bloco(c, bloco, largura, altura):

    texto = bloco["texto"]

    x = (
        bloco["left"] / 100
    ) * largura

    largura_bloco = (
        bloco["width"] / 100
    ) * largura

    y_top = (
        bloco["top"] / 100
    ) * altura

    altura_bloco = (
        bloco["height"] / 100
    ) * altura

    tamanho_fonte = calcular_fonte(
        bloco,
        altura
    )

    if bloco["titulo"]:
        fonte = FONTE_NEGRITO
    else:
        fonte = FONTE_NORMAL

    c.setFont(
        fonte,
        tamanho_fonte
    )

    # -----------------------------------------------------
    # Divide o texto em linhas
    # -----------------------------------------------------

    palavras = texto.split()

    linhas = []
    linha = ""

    for palavra in palavras:

        tentativa = (
            palavra
            if not linha
            else linha + " " + palavra
        )

        largura_texto = c.stringWidth(
            tentativa,
            fonte,
            tamanho_fonte
        )

        if largura_texto <= largura_bloco:
            linha = tentativa

        else:
            if linha:
                linhas.append(linha)

            linha = palavra

    if linha:
        linhas.append(linha)

    # -----------------------------------------------------
    # Desenha de cima para baixo
    # -----------------------------------------------------

    leading = tamanho_fonte * 1.15

    y = altura - y_top - tamanho_fonte

    limite_inferior = (
        altura
        - y_top
        - altura_bloco
    )

    for linha in linhas:

        if y < limite_inferior:
            break

        c.drawString(
            x,
            y,
            linha
        )

        y -= leading


# ---------------------------------------------------------
# CRIA PDF
# ---------------------------------------------------------

def criar_pdf(paginas):

    print()
    print("Criando PDF...")
    print()

    primeira_largura = paginas[0]["largura"]
    primeira_altura = paginas[0]["altura"]

    proporcao = (
        primeira_altura /
        primeira_largura
    )

    # largura do PDF em pontos
    largura_pdf = 600

    altura_pdf = (
        largura_pdf *
        proporcao
    )

    c = canvas.Canvas(
        PDF_FINAL,
        pagesize=(
            largura_pdf,
            altura_pdf
        )
    )
    for indice, pagina in enumerate(paginas, 1):

        print(
            f"Montando página {indice}/6..."
        )

        svg_png = pagina["png"]

        # -------------------------------------------------
        # Fundo SVG
        # -------------------------------------------------

        if os.path.exists(svg_png):

            try:
                c.drawImage(
                    svg_png,
                    0,
                    0,
                    width=largura_pdf,
                    height=altura_pdf,
                    preserveAspectRatio=True,
                    anchor="c",
                    mask="auto"
                )

            except Exception as e:
                print(
                    f"AVISO: erro no fundo: {e}")
                
            

        # -------------------------------------------------
        # Texto selecionável
        # -------------------------------------------------
        # Define o texto como transparente para não encavalar com o texto da imagem de fundo
        c.setFillColor(black, alpha=0.0)

        for bloco in pagina["blocos"]:

            desenhar_bloco(
                c,
                bloco,
                largura_pdf,
                altura_pdf
            )

        c.showPage()

    c.save()

    print()
    print("=" * 60)
    print("PDF FINALIZADO")
    print("=" * 60)
    print()
    print(
        os.path.abspath(PDF_FINAL)
    )
    print()


# ---------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------

def main():

    paginas = []

    for numero in range(1, 7):

        print()
        print(
            f"========== PÁGINA {numero} =========="
        )

        svg_url = (
            f"{BASE}/page_{numero}.svg"
            f"?v={VERSAO}"
        )

        html_url = (
            f"{BASE}/page_{numero}.html"
            f"?v={VERSAO}"
        )

        svg_arquivo = os.path.join(
            PASTA,
            f"page_{numero}.svg"
        )

        html_arquivo = os.path.join(
            PASTA,
            f"page_{numero}.html"
        )

        png_arquivo = os.path.join(
            PASTA,
            f"page_{numero}.png"
        )

        # -------------------------------------------------
        # SVG
        # -------------------------------------------------

        try:

            svg_bytes = baixar(
                svg_url,
                svg_arquivo
            )

            largura, altura = descobrir_tamanho_svg(
                svg_bytes
            )

            print(
                f"Tamanho detectado: "
                f"{largura} x {altura}"
            )

        except Exception as e:

            print(
                f"ERRO no SVG da página "
                f"{numero}: {e}"
            )

            continue

        # -------------------------------------------------
        # HTML
        # -------------------------------------------------

        try:

            html_bytes = baixar(
                html_url,
                html_arquivo
            )

            blocos = extrair_blocos(
                html_bytes
            )

            print(
                f"Blocos de texto encontrados: "
                f"{len(blocos)}"
            )

        except Exception as e:

            print(
                f"ERRO no HTML da página "
                f"{numero}: {e}"
            )

            blocos = []

        # -------------------------------------------------
        # PNG do SVG
        # -------------------------------------------------

        print("Convertendo SVG para imagem...")

        converter_svg_para_png(
            svg_arquivo,
            png_arquivo
        )

        paginas.append({
            "numero": numero,
            "largura": largura,
            "altura": altura,
            "blocos": blocos,
            "png": png_arquivo
        })

    # -----------------------------------------------------
    # Confere
    # -----------------------------------------------------

    if not paginas:

        print(
            "Nenhuma página foi baixada."
        )

        return

    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    criar_pdf(paginas)


if __name__ == "__main__":
    main()
