import re
import requests
from pathlib import Path

BASE = "https://online.fliphtml5.com/topview/tfxa/"

ARQUIVOS = {
    "config.js": BASE + "javascript/config.js?1791498966",
    "resource_skeleton.js": (
        "https://static.fliphtml5.com/resourceFiles/"
        "html5_templates/template/Popular/resource_skeleton.js"
        "?1791498966"
    ),
}

sessao = requests.Session()
sessao.headers["User-Agent"] = "Mozilla/5.0"

for nome, url in ARQUIVOS.items():
    print("\n" + "=" * 75)
    print("ARQUIVO:", nome)

    try:
        resposta = sessao.get(url, timeout=30)
        print("STATUS:", resposta.status_code)
        print("TIPO:", resposta.headers.get("Content-Type"))
        resposta.raise_for_status()

        texto = resposta.text
        Path(nome).write_text(texto, encoding="utf-8")

        print("TAMANHO:", len(texto), "caracteres")
        print("SALVO EM:", Path(nome).resolve())

        # Mostra ocorrências relevantes e o contexto ao redor
        padrao = re.compile(
            r"config|page|pages|book|flip|large|webp|"
            r"json|xml|data|resource|total|count|manifest",
            re.IGNORECASE,
        )

        linhas = texto.splitlines()
        encontradas = 0

        for numero, linha in enumerate(linhas, start=1):
            if padrao.search(linha):
                print(f"L{numero}: {linha[:350]}")
                encontradas += 1

                if encontradas >= 60:
                    print("... limite de linhas relevantes atingido")
                    break

        # Lista caminhos de recursos mencionados no arquivo
        urls = sorted(set(re.findall(
            r"""https?://[^"'\\\s<>]+|"""
            r"""(?<![A-Za-z0-9])(?:javascript|files)/[^"'\\\s<>]+""",
            texto,
        )))

        if urls:
            print("\nREFERÊNCIAS ENCONTRADAS:")
            for item in urls[:50]:
                print(" ", item)

    except requests.RequestException as erro:
        print("ERRO:", erro)

print("\nDiagnóstico concluído.")
