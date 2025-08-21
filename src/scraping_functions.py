import re
import requests
from bs4 import BeautifulSoup

def extrair_regiao(source):
    municipio = source.find("p", class_="title").text
    municipio_formatado = re.match(r"^(?:Indicadores por localidade - )(.+?)(?: \(Município\))$", municipio)

    if(municipio_formatado):
        texto_extraido = municipio_formatado.group(1)
        return texto_extraido
    else:
        return None

def extrair_data(source):
    tr_data = source.find("tr", class_="table-simple--header")
    td_data = tr_data.find_all("td")
    
    anos = [data.text for data in td_data][1:]
    return anos

def extrair_populacao(source):
    tr_populacao = source.find_all("tr",class_="table-simple--row")[0]
    td_populacao = tr_populacao.find_all("td")
    populacao = [pop.text for pop in td_populacao][1:]
    return populacao

def extrair_tipo(source):
    municipio = source.find("p", class_="title").text
    municipio_formatado = re.match(r"Indicadores por localidade - .+\((.+)\)", municipio)

    if(municipio_formatado):
        texto_extraido = municipio_formatado.group(1)
        resultado = texto_extraido.replace("(","").replace(")","")
        return texto_extraido

def extrair_esgoto(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=3&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    tr_esgoto = soup.find_all("tr",class_="table-simple--row")[9]
    tds = tr_esgoto.find_all("td")[1:]
    infos = [data.text for data in tds]
    return infos

def extrair_doencas(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=6&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    trs = soup.find_all("tr", class_="table-simple--row")
    tr_linhas = [trs[4], trs[5], trs[7], trs[8],trs[10]]
    
    infos = []
    for tr in tr_linhas:
        valores = [td.get_text(strip=True) for td in tr.find_all("td")[1:]]
        infos.append(valores)    
    
    dict_infos = {
        "internacao_hidrica": infos[0],
        "internacao_diarreia": infos[1],
        "internacao_dengue": infos[2],
        "internacao_leptospirose": infos[3],
        "internacao_esquistossomose": infos[4]
    }
    return dict_infos

def extrair_obitos(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=8&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    trs = soup.find_all("tr", class_="table-simple--row")[11]
    tds = trs.find_all("td")[1:]
    infos = [data.text for data in tds]
    return infos
