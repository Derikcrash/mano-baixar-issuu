# Importa Image da biblioteca Pillow.
# Ela permite abrir, manipular e converter imagens.
from PIL import Image

# Importa Path, que facilita trabalhar com caminhos de pastas e arquivos.
from pathlib import Path

# Importa argparse, que permite receber informações pelo terminal.
# Por exemplo: qual pasta converter e qual nome dar ao PDF.
import argparse


# Define uma função chamada converter_para_pdf.
# Ela recebe dois argumentos:
# - pasta_entrada: a pasta onde estão as imagens.
# - nome_pdf: o nome do PDF que será criado.
# O nome do PDF tem um valor padrão: "livro.pdf".
def converter_para_pdf(pasta_entrada, nome_pdf="livro.pdf"):

    # Transforma o caminho recebido em um objeto Path.
    # Isso facilita verificar se a pasta existe e acessar seus arquivos.
    pasta = Path(pasta_entrada)

    # Verifica se o caminho informado realmente é uma pasta existente.
    if not pasta.is_dir():

        # Exibe uma mensagem de erro caso a pasta não exista.
        print(f"Erro: a pasta não existe: {pasta}")

        # Encerra a função para não tentar converter arquivos inexistentes.
        return

    # Cria um conjunto com as extensões de imagem que serão aceitas.
    # O ponto faz parte da extensão, por exemplo, ".png".
    extensoes = {".png", ".jpg", ".jpeg", ".webp"}

    # Procura os arquivos que estão diretamente dentro da pasta.
    # Não procura automaticamente em subpastas.
    # Também ignora arquivos que não tenham uma das extensões aceitas.
    arquivos = sorted(
        arquivo
        for arquivo in pasta.iterdir()
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes
    )

    # Se a lista estiver vazia, nenhuma imagem foi encontrada.
    if not arquivos:

        # Informa o problema ao usuário.
        print("Nenhuma imagem encontrada na pasta.")

        # Encerra a função, pois não há imagens para converter.
        return

    # Cria uma lista vazia para guardar as imagens abertas.
    imagens = []

    # O try permite tratar erros que possam ocorrer durante a conversão.
    try:

        # Percorre cada arquivo encontrado na pasta.
        for arquivo in arquivos:

            # Abre a imagem.
            # O with garante que o arquivo original seja fechado após a leitura.
            with Image.open(arquivo) as imagem:

                # Converte a imagem para RGB.
                # Esse formato é adequado para criar o PDF e evita problemas
                # com transparência ou modos de cor incompatíveis.
                # O resultado é guardado na lista imagens.
                imagens.append(imagem.convert("RGB"))

        # Monta o caminho completo do PDF de saída.
        # O PDF será salvo dentro da pasta que contém as imagens.
        # Exemplo: imagens/livro.pdf
        destino = pasta / nome_pdf

        # Salva a primeira imagem como a primeira página do PDF.
        # save_all=True permite incluir outras páginas no mesmo arquivo.
        # append_images adiciona todas as imagens restantes como páginas.
        imagens[0].save(
            destino,
            "PDF",
            save_all=True,
            append_images=imagens[1:]
        )

        # Mostra o caminho completo do PDF criado.
        # resolve() transforma o caminho em um caminho absoluto.
        print(f"\nPDF criado: {destino.resolve()}")

        # Mostra quantas páginas foram incluídas no PDF.
        print(f"Total de páginas: {len(imagens)}")

    # Se ocorrer um erro durante a abertura ou conversão,
    # o programa mostra a mensagem do erro em vez de simplesmente parar.
    except Exception as erro:
        print(f"Erro durante a conversão: {erro}")

    # O finally é executado mesmo se ocorrer um erro.
    # Aqui, fechamos as imagens que foram carregadas na memória.
    finally:
        for imagem in imagens:
            imagem.close()


# Esta condição verifica se o arquivo está sendo executado diretamente.
# Assim, a função também pode ser importada por outro script
# sem iniciar automaticamente a leitura dos argumentos do terminal.
if __name__ == "__main__":

    # Cria o interpretador dos argumentos recebidos pelo terminal.
    parser = argparse.ArgumentParser(
        description="Converte imagens de uma pasta em um único PDF."
    )

    # Define o primeiro argumento obrigatório.
    # Ele informa a pasta onde estão as imagens.
    # Exemplo: python converter.py imagens
    parser.add_argument(
        "pasta",
        help="Pasta que contém as imagens"
    )

    # Define um argumento opcional para escolher o nome do PDF.
    # -o e --saida são duas formas de informar o mesmo argumento.
    # Se o usuário não informar um nome, será usado "livro.pdf".
    parser.add_argument(
        "-o", "--saida",
        default="livro.pdf",
        help="Nome do PDF de saída (padrão: livro.pdf)"
    )

    # Lê os argumentos digitados no terminal.
    # Os valores ficam disponíveis em args.pasta e args.saida.
    args = parser.parse_args()

    # Executa a função usando os valores recebidos.
    # args.pasta indica onde estão as imagens.
    # args.saida indica o nome do PDF que será criado.
    converter_para_pdf(args.pasta, args.saida)