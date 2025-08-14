from bs4 import BeautifulSoup
from scraping_functions import extrair_regiao, extrair_data, extrair_populacao, extrair_tipo,extrair_dhidrica
import requests

def extrarir_municipio_info():
    for i in range(350010,355715,5):
        r = requests.get(f'https://www.painelsaneamento.org.br/explore/localidade?SE[l]={i}&page=1&ajax=ajax')
        soup = BeautifulSoup(r.content, 'lxml')

        regiao = extrair_regiao(soup)
        print(regiao)
        if regiao is not None:
            extrair_data(soup)
            extrair_populacao(soup)
            extrair_tipo(soup)
        print(f"🔍 Coleta do municipio {regiao} concluida!")

        extrair_indicadores(i)

def extrair_indicadores(i):
    extrair_dhidrica(i)
    #extrair_ddiarreia(i)

extrarir_municipio_info()