from bs4 import BeautifulSoup
from scraping_functions import extrair_regiao, extrair_data, extrair_populacao,extrair_tipo, extrair_esgoto, extrair_doencas, extrair_obitos
import requests

def extrair_municipio_info():

    for i in range(350010,355715,5):
        r = requests.get(f'https://www.painelsaneamento.org.br/explore/localidade?SE[l]={i}&page=1&ajax=ajax')
        soup = BeautifulSoup(r.content, 'lxml')
        regiao = extrair_regiao(soup)

        if regiao is not None:
            extrair_data(soup)
            extrair_populacao(soup)
            extrair_tipo(soup)
            extrair_indicadores(i)
            print(f"🔍 Coleta do municipio {regiao} concluida!")

def extrair_indicadores(i):
    indicadores = extrair_doencas(i)
    indicadores["coleta_de_esgoto"] = extrair_esgoto(i)
    indicadores["obitos_doenca_respiratoria"] = extrair_obitos(i)

extrair_municipio_info()