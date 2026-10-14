import os
import requests

# Pasta onde as páginas serão salvas
PASTA = "imagens"
os.makedirs(PASTA, exist_ok=True)

# Parte fixa do endereço
BASE_URL = "https://ps.calameoassets.com/261008210744-c2588ee7430b2ee2679a845f0e3d9d28/p{}.svgz"

# Token de acesso fornecido nos links
TOKEN = (
    "exp=1791955493~acl=%2F261008210744-c2588ee7430b2ee2679a845f0e3d9d28%2F%2A"
    "~hmac=21c1421f4fbb35cb68fb451732804ff21c36e0037b3e0446468e6c436c69694a"
)

# Cabeçalhos para a requisição
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Baixar páginas de 1 até 20
for pagina in range(1, 21):
    url = f"{BASE_URL.format(pagina)}?_token_={TOKEN}"
    arquivo = os.path.join(PASTA, f"pagina_{pagina}.svgz")

    try:
        print(f"Baixando página {pagina}/20...")

        resposta = requests.get(
            url,
            headers=headers,
            timeout=30
        )
        resposta.raise_for_status()

        with open(arquivo, "wb") as f:
            f.write(resposta.content)

        print(f"Salvo: {arquivo}")

    except requests.RequestException as erro:
        print(f"Erro na página {pagina}: {erro}")

print("\nDownload concluído!")