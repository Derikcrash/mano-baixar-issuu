import requests
import re
import base64

url = "https://investidorinstitucional.com.br/edicoes-anteriores-em-pdf/"

html = requests.get(url).text

padrao = r"FB3D_CLIENT_DATA\.push\('([^']+)'\)"

resultado = re.search(padrao, html)

if resultado:
    base64_data = resultado.group(1)
    print(base64_data)
else:
    print("Não encontrou")
    
decodificado = base64.b64decode(padrao)