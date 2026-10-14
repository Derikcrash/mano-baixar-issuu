import requests
import re
import base64
import json

url_pagina = "https://investidorinstitucional.com.br/edicoes-anteriores-em-pdf/"
html = requests.get(url_pagina).text

padrao = r"FB3D_CLIENT_DATA\.push\('([^']+)'\)"
dados = re.findall(padrao, html)    

codigo = dados[1]

decodificado = base64.b64decode(codigo)
 
json_data = json.loads(decodificado)

post = list(json_data["posts"].values())[0]

titulo = post["title"]
pdf_url = post["data"]["guid"]

pdf = requests.get(pdf_url).content

with open(f"{titulo}.pdf", "wb") as arquivo:
    arquivo.write(pdf)

print(f"Baixado: {titulo}.pdf")
