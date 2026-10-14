import requests
from PIL import Image
from io import BytesIO
import cairosvg
import os

base_url = "https://brasilenergia.z21.web.core.windows.net/flip/1095/e0feeb4165b54b23bd2266158db56a73/Bia506/"
token = "?uni=0a37d46df7f7cf6862f01b1296af542f"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

total_paginas = 87
imagens_pdf = []

print(f"[*] Iniciando montagem avançada de {total_paginas} páginas (Camada Base + Camada de Texto SVG)...")

for pagina in range(1, total_paginas + 1):
    num_str = f"{pagina:04d}"
    print(f"    -> Processando página {pagina}/{total_paginas}...")
    
    url_fundo = f"{base_url}files/assets/common/page-html5-substrates/page{num_str}_2.jpg{token}"
    url_texto = f"{base_url}files/assets/common/page-vectorlayers/{num_str}.svg{token}"
    
    req_fundo = requests.get(url_fundo, headers=headers)
    if req_fundo.status_code != 200:
        print(f"       [!] Erro: Fundo da página {pagina} não encontrado.")
        continue
        
    img_fundo = Image.open(BytesIO(req_fundo.content)).convert('RGBA')
    
    req_texto = requests.get(url_texto, headers=headers)
    if req_texto.status_code == 200:
        try:
            png_bytes = cairosvg.svg2png(bytestring=req_texto.content)
            img_texto = Image.open(BytesIO(png_bytes)).convert('RGBA')
            
            img_texto = img_texto.resize(img_fundo.size, Image.Resampling.LANCZOS)
            
            img_fundo = Image.alpha_composite(img_fundo, img_texto)
        except Exception as e:
            print(f"       [!] Erro ao renderizar SVG da página {pagina}. Salvando só o fundo. Erro: {e}")
    else:
        print(f"       [!] Aviso: SVG não encontrado para a página {pagina}. Usando apenas o fundo.")
        
    imagens_pdf.append(img_fundo.convert('RGB'))

if imagens_pdf:
    nome_pdf = "brasil_energia_montada_com_texto.pdf"
    print(f"\n[*] Compilando todas as camadas no arquivo {nome_pdf}...")
    
    imagens_pdf[0].save(
        nome_pdf, 
        save_all=True, 
        append_images=imagens_pdf[1:]
    )
    print(f"[*] Sucesso absoluto! Revista capturada, montada e salva em: {os.path.abspath(nome_pdf)}")
else:
    print("[!] Nenhuma página foi processada com sucesso.")
    