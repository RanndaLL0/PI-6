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

def extrair_tipo(source):
    municipio = source.find("p", class_="title").text
    municipio_formatado = re.match(r"Indicadores por localidade - .+\((.+)\)", municipio)

    if(municipio_formatado):
        texto_extraido = municipio_formatado.group(1)
        resultado = texto_extraido.replace("(","").replace(")","")
        return texto_extraido
    
def extrair_fato(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=1&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    trs = soup.find_all("tr", class_="table-simple--row")
    data = [trs[0],trs[3],trs[5],trs[7],trs[8],trs[11],trs[12]]
    
    infos = []
    for tr in data:
        valores = [td.get_text(strip=True) for td in tr.find_all("td")[1:]]
        infos.append(valores)
    
    
       
    return {
        "populacao": infos[0],
        "moradias": infos[1],
        "densidade_domiciliar": infos[2],
        "pib_absoluto": infos[3],
        "pib_per_capita": infos[4],
        "area_do_municipio": infos[5],
        "densidade_demografica": infos[6]
    }

def extrair_coleta_esgoto(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=3&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    trs = soup.find_all("tr", class_="table-simple--row")
    tr_linhas = [trs[0], trs[3], trs[4],trs[9],trs[10]]
    
    infos = []
    for tr in tr_linhas:
        valores = [td.get_text(strip=True) for td in tr.find_all("td")[1:]]
        infos.append(valores)
    
    dict_infos = {
        "populacao_sem_coleta_de_esgoto": infos[0],
        "populacao_urbana_com_coleta": infos[1],
        "populacao_urbana_sem_coleta": infos[2],
        "esgoto_coletado": infos[3],
        "esgoto_tratado": infos[4],
    }
    return dict_infos

def extrair_coleta_agua(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=2&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    trs = soup.find_all("tr", class_="table-simple--row")
    tr_linhas = [trs[2], trs[3], trs[6],trs[7] ,trs[10],trs[11]]
    
    infos = []
    for tr in tr_linhas:
        valores = [td.get_text(strip=True) for td in tr.find_all("td")[1:]]
        infos.append(valores)
    
    dict_infos = {
        "recebimento_regular_de_agua": infos[0],
        "recebimento_irregular_de_agua": infos[1],
        "populacao_com_acesso_a_agua": infos[2],
        "populacao_sem_acesso_a_agua": infos[3],
        "populacao_urbana_com_acesso_a_agua": infos[4],
        "populacao_urbana_sem_acesso_a_agua": infos[5],
    }
    return dict_infos

def extrair_receita(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=4&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    trs = soup.find_all("tr", class_="table-simple--row")
    tr_linhas = [trs[2], trs[3], trs[4]]
    
    infos = []
    for tr in tr_linhas:
        valores = [td.get_text(strip=True) for td in tr.find_all("td")[1:]]
        infos.append(valores)
    
    dict_infos = {
        "receita_direta_agua": infos[1],
        "receita_direta_esgoto": infos[2],
        "receita_direta_total": infos[3],
    }
    return dict_infos

def extrair_internacoes(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=5&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    trs = soup.find_all("tr", class_="table-simple--row")
    tr_linhas = [trs[0], trs[1], trs[2], trs[3],trs[6],trs[7]]
    
    infos = []
    for tr in tr_linhas:
        valores = [td.get_text(strip=True) for td in tr.find_all("td")[1:]]
        infos.append(valores)    
    
    dict_infos = {
        "internacao_dengue": infos[0],
        "internacao_leptospirose": infos[1],
        "internacao_malaria": infos[2],
        "internacao_infantil": infos[3],
        "internacao_adolecencia": infos[4]
    }
    return dict_infos

def extrair_obitos(i):
    re = requests.get(f"https://www.painelsaneamento.org.br/explore/localidade?SE%5Bl%5D={i}&page=8&ajax=ajax")
    soup = BeautifulSoup(re.content, 'lxml')
    trs = soup.find_all("tr", class_="table-simple--row")
    tr_linhas = [trs[8],trs[11],trs[7],trs[12]]
    
    infos = []
    for tr in tr_linhas:
        valores = [td.get_text(strip=True) for td in tr.find_all("td")[1:]]
        infos.append(valores)  
        
    return {
        "obitos_doenca_respiratoria_cem": infos[1],
        "obitos_doenca_respiratoria_abs": infos[0],
        "custo_internacao_doenca_respiratoria": infos[2],
        "obitos_doenca_respiratoria_infantil": infos[3]
    }
