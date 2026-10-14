import json
import requests
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO
# ============================================================

ARQUIVO_EDICOES = "edicoes_encontradas.json"
PASTA_PDFS = Path("pdfs")

PASTA_PDFS.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}


# ============================================================
# LER EDIÇÕES ENCONTRADAS
# ============================================================

with open(
    ARQUIVO_EDICOES,
    "r",
    encoding="utf-8"
) as arquivo:

    edicoes = json.load(arquivo)


print("=" * 60)
print("DOWNLOAD DE TESTE — 1 PDF")
print("=" * 60)

print(f"\nTotal de edições disponíveis: {len(edicoes)}")


# ============================================================
# PEGAR SOMENTE A PRIMEIRA
# ============================================================

edicao = edicoes[1]

titulo = edicao["titulo"]
url = edicao["pdf"]

print(f"\nEdição selecionada: {titulo}")
print(f"Páginas: {edicao['paginas']}")
print(f"URL: {url}")


# ============================================================
# NOME DO ARQUIVO
# ============================================================

nome = titulo

# Remove caracteres que podem dar problema no nome do arquivo
for caractere in '/\\:*?"<>|':

    nome = nome.replace(caractere, "_")


caminho = PASTA_PDFS / f"{nome}.pdf"


# ============================================================
# DOWNLOAD
# ============================================================

print("\n[+] Baixando PDF...")

try:

    resposta = requests.get(
        url,
        headers=HEADERS,
        timeout=120
    )

    resposta.raise_for_status()

except requests.RequestException as erro:

    print(f"\n[ERRO] Não foi possível baixar:")
    print(erro)

    raise SystemExit(1)


# ============================================================
# VERIFICAR SE É REALMENTE PDF
# ============================================================

if not resposta.content.startswith(b"%PDF"):

    print("\n[ERRO] O arquivo baixado não parece ser um PDF.")

    print(
        "Primeiros bytes recebidos:",
        resposta.content[:100]
    )

    raise SystemExit(1)


# ============================================================
# SALVAR
# ============================================================

caminho.write_bytes(resposta.content)


tamanho_mb = len(resposta.content) / (1024 * 1024)


print("\n[OK] Download concluído!")
print(f"Arquivo: {caminho}")
print(f"Tamanho: {tamanho_mb:.2f} MB")

print("\n" + "=" * 60)
print("TESTE CONCLUÍDO")
print("=" * 60)
