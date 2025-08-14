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

def extrair_populacao(source):
    tr_populacao = source.find_all("tr",class_="table-simple--row")[0]
    td_populacao = tr_populacao.find_all("td")
    populacao = [pop.text for pop in td_populacao][1:]

def extrair_tipo(source):
    municipio = source.find("p", class_="title").text
    municipio_formatado = re.match(r"Indicadores por localidade - .+\((.+)\)", municipio)

    if(municipio_formatado):
        texto_extraido = municipio_formatado.group(1)
        resultado = texto_extraido.replace("(","").replace(")","")
        return texto_extraido
    
def extrair_dhidrica(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=6&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    tr_hidrica = soup.find_all("tr",class_="table-simple--row")[4]
    tds = tr_hidrica.find_all("td")[1:]
    infos = [data.text for data in tds]
    return infos

def extrair_ddiarreia(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=6&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    tr_diareia = soup.find_all("tr",class_="table-simple--row")[5]
    tds = tr_diareia.find_all("td")[1:]
    infos = [data.text for data in tds]
    return infos

def extrair_ddengue(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=6&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    tr_dengue = soup.find_all("tr",class_="table-simple--row")[7]
    tds = tr_dengue.find_all("td")[1:]
    infos = [data.text for data in tds]
    return infos

def extrair_leptospirose(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=6&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    tr_leptospirose = soup.find_all("tr",class_="table-simple--row")[8]
    tds = tr_leptospirose.find_all("td")[1:]
    infos = [data.text for data in tds]
    return infos

def extrair_esgoto(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=3&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    tr_esgoto = soup.find_all("tr",class_="table-simple--row")[9]
    tds = tr_esgoto.find_all("td")[1:]
    infos = [data.text for data in tds]
    return infos