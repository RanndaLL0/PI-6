from bs4 import BeautifulSoup
from scraping_functions import (extrair_regiao
                                ,extrair_data
                                ,extrair_fato
                                ,extrair_tipo
                                ,extrair_coleta_agua
                                ,extrair_coleta_esgoto
                                ,extrair_internacoes
                                ,extrair_obitos)
import requests
import json

class scraper:
    def __init__(self,output_file="./roraima.json"):
        self.output_file = output_file
        self.resultados = []
        pass
        
    def extrair_info(self):
        for i in range(140004,140075,1):
            r = requests.get(f'https://www.painelsaneamento.org.br/explore/localidade?SE[l]={i}&page=1&ajax=ajax')
            soup = BeautifulSoup(r.content, 'lxml')
            
            info_area = {}
            regiao = extrair_regiao(soup)
            if regiao is not None:
                info_area["regiao"] = regiao
                info_area["data"] = extrair_data(soup)
                info_area["area"] = extrair_tipo(soup)
                info_area["fato"] = extrair_fato(i)
                self.extrair_indicadores(i,info_area)
                print(f"🔍 Coleta do municipio {info_area["regiao"]} concluida!")
                self.resultados.append(info_area)
                self.salvar_resultado()

    def extrair_indicadores(self,i,info_area):
        info_area["internacoes"] = extrair_internacoes(i)
        info_area["coleta_esgoto"] = extrair_coleta_esgoto(i)
        info_area["coleta_agua"] = extrair_coleta_agua(i)
        info_area["incidenca_obitos_doenca_respiratoria"] = extrair_obitos(i)
        
    def salvar_resultado(self):
        with open(self.output_file,"w",encoding="utf-8") as f:
            json.dump(self.resultados,f,ensure_ascii=False, indent=4)

scraping = scraper()
scraping.extrair_info()