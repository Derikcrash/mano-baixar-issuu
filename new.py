indicator = ''''''
extra = ''''''

import re
import requests
from bs4 import BeautifulSoup
from loguru import logger


def extract_news_info(**kwargs):
    extracted_info = kwargs.get('extracted_info', {})

    logger.debug('------ INICIANDO SCRIPT --------')

    try:
        if extracted_info.get('content'):
            texto_content = extracted_info['content']


            pattern_comeco = [
                r'Adicione como fonte preferencial no Google'
            ]

            texto_content = re.split(
                '|'.join(pattern_comeco),
                texto_content,
                flags=re.IGNORECASE
            )[-1].strip()


            pattern_fim = [
                r'Eleições 2026:'
            ]

            clean_content = re.split(
                '|'.join(pattern_fim),
                texto_content,
                flags=re.IGNORECASE
            )[0].strip()

            extracted_info['content'] = clean_content

        else:
            logger.warning("Não tem content")

    except Exception as e:
        logger.error(f'Erro ao extrair informações: {e}')

    return extracted_info


if __name__ == "__main__":
    url_noticia = "https://noticias.r7.com/rio-de-janeiro/rj-no-ar/video/acao-do-detran-e-pm-descobre-ferro-velho-clandestino-e-prende-responsavel-em-santissimo-no-rio-23092026/"

    html = requests.get(url_noticia).text
    soup = BeautifulSoup(html, 'html.parser')
    texto_feio = "\n".join(
        [p.get_text() for p in soup.find_all('p')]
    )

    resultado = extract_news_info(
        extracted_info={"content": texto_feio}
    )

    print(resultado["content"])