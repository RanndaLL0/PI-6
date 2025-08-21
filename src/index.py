from bs4 import BeautifulSoup
from scraping_functions import extrair_regiao, extrair_data, extrair_populacao,extrair_tipo, extrair_esgoto, extrair_doencas, extrair_obitos
import requests


class scraper:
    def __init__(self):
        self.info_area = {}

    def extrair_info(self):
        for i in range(350010,355715,5):
            r = requests.get(f'https://www.painelsaneamento.org.br/explore/localidade?SE[l]={i}&page=1&ajax=ajax')
            soup = BeautifulSoup(r.content, 'lxml')
            regiao = extrair_regiao(soup)

            if regiao is not None:
                self.info_area["data"] = extrair_data(soup)
                self.info_area["populacao"] = extrair_populacao(soup)
                self.info_area["area"] = extrair_tipo(soup)
                self.extrair_indicadores(i)
                print(f"🔍 Coleta do municipio {regiao} concluida!")

    def extrair_indicadores(self,i):
        self.info_area["doencas"] = extrair_doencas(i)
        self.info_area["coleta_de_esgoto"] = extrair_esgoto(i)
        self.info_area["incidenca_obitos_doenca_respiratoria"] = extrair_obitos(i)
        self.info_area["valores"] = extrair_obitos(i)
        print(self.info_area)


scraping = scraper()
scraping.extrair_info()

