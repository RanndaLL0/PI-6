from bs4 import BeautifulSoup
from scraping_functions import extrair_regiao, extrair_data, extrair_populacao,extrair_tipo,extrair_dhidrica,extrair_ddiarreia,extrair_ddengue, extrair_esgoto
import requests

def extrarir_municipio_info():

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
    extrair_dhidrica(i)
    extrair_ddiarreia(i)
    extrair_ddengue(i)
    extrair_esgoto(i)

extrarir_municipio_info()