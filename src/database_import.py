import os
import json
import httpx
import time
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

class Import:
    def __init__(self, origin: str):
        self.supabaseClient: Client
        self.origin_directory: str = origin
        self.BATCH_SIZE = 200

    def init_connection(self, url: str, key: str):
        self.supabaseClient = create_client(url, key)

    def insert_ano(self):
        anos = [str(y) for y in range(2010, 2024)]
        for ano in anos:
            self.supabaseClient.table("ano").insert({"ano": ano}).execute()

    def parse_number(self, value: str):
        if value in ("-", None, ""):
            return None
        value = str(value).replace(".", "").replace(",", ".")
        try:
            return int(float(value))
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return None

    def __process_area(self, file):
        area = os.path.splitext(file)[0]
        print(f"Área processada: {area}")
        try:
            response = (
                self.supabaseClient.table("area")
                .insert({"nome": area})
                .execute()
            )
            return response.data[0]["id"]
        except Exception as err:
            print(f"Erro inesperado ao processar área '{area}': {err}")
            return None

    def __process_regiao(self, regiao, area_id):
        nome = regiao["regiao"]
        tipo = regiao["area"]
        area_val = self.parse_number(regiao["fato"]["area_do_municipio"][0])
        try:
            response = (
                self.supabaseClient.table("regiao")
                .insert({
                    "nome": nome,
                    "area_id": area_id,
                    "area_km2": area_val,
                    "tipo_area": tipo
                })
                .execute()
            )
            return response.data[0]["id"]
        except Exception as err:
            print(f"Erro inesperado ao processar região '{nome}': {err}")
            return None

    def __insert_bulk(self, table_name, data):
        for i in range(0, len(data), self.BATCH_SIZE):
            chunk = data[i:i + self.BATCH_SIZE]
            for attempt in range(3):
                try:
                    self.supabaseClient.table(table_name).insert(chunk).execute()
                    break
                except Exception as e:
                    print(f"Erro ao inserir lote ({table_name}) tentativa {attempt+1}: {e}")
                    time.sleep(2)

    def import_to_supabase(self):
        
        for file in os.listdir(self.origin_directory):
            
            if not file.endswith(".json"):
                continue
            
            area_id = self.__process_area(file)
            
            if not area_id:
                continue
            
            path = os.path.join(self.origin_directory, file)
            data = json.load(open(path, encoding="utf-8"))
            
            print(f"\nIniciando importação do arquivo {file}")
            fatos_bulk, internacoes_bulk, coleta_bulk, doencas_bulk = [], [], [], []
            
            for regiao in data:
                
                regiao_id = self.__process_regiao(regiao, area_id)
                
                if not regiao_id:
                    continue
                
                for i, ano in enumerate(regiao["data"]):
                    
                    ano_row = (
                        self.supabaseClient.table("ano")
                        .select("id")
                        .eq("ano", str(ano))
                        .execute()
                    )
                    
                    if not ano_row.data:
                        continue
                    ano_id = ano_row.data[0]["id"]
                    
                    fatos_bulk.append({
                        "regiao_id": regiao_id,
                        "ano_id": ano_id,
                        "populacao": self.parse_number(regiao["fato"]["populacao"][i]),
                        "moradias": self.parse_number(regiao["fato"]["moradias"][i]),
                        "densidade_domiciliar": self.parse_number(regiao["fato"]["densidade_domiciliar"][i]),
                        "pib_absoluto": self.parse_number(regiao["fato"]["pib_absoluto"][i]),
                        "pib_per_capita": self.parse_number(regiao["fato"]["pib_per_capita"][i]),
                        "densidade_demografica": self.parse_number(regiao["fato"]["densidade_demografica"][i]),
                    })
                    
                    internacoes_bulk.append({
                        "regiao_id": regiao_id,
                        "ano_id": ano_id,
                        "dengue": self.parse_number(regiao["internacoes"]["internacao_dengue"][i]),
                        "leptospirose": self.parse_number(regiao["internacoes"]["internacao_leptospirose"][i]),
                        "malaria": self.parse_number(regiao["internacoes"]["internacao_malaria"][i]),
                        "infantil": self.parse_number(regiao["internacoes"]["internacao_infantil"][i]),
                        "adolescencia": self.parse_number(regiao["internacoes"]["internacao_adolecencia"][i]),
                    })
                    
                    coleta_bulk.append({
                        "regiao_id": regiao_id,
                        "ano_id": ano_id,
                        "pop_sem_coleta": self.parse_number(
                            regiao["coleta_esgoto"]["populacao_sem_coleta_de_esgoto"][i]
                        ),
                        "pop_urbana_com_coleta": self.parse_number(
                            regiao["coleta_esgoto"]["populacao_urbana_com_coleta"][i]
                        ),
                        "pop_urbana_sem_coleta": self.parse_number(
                            regiao["coleta_esgoto"]["populacao_urbana_sem_coleta"][i]
                        ),
                        "esgoto_coletado": self.parse_number(
                            regiao["coleta_esgoto"]["esgoto_coletado"][i]
                        ),
                        "esgoto_tratado": self.parse_number(
                            regiao["coleta_esgoto"]["esgoto_tratado"][i]
                        ),
                    })
                    
                    doencas_bulk.append({
                        "regiao_id": regiao_id,
                        "ano_id": ano_id,
                        "obitos_cem": self.parse_number(
                            regiao["incidenca_obitos_doenca_respiratoria"]["obitos_doenca_respiratoria_cem"][i]
                        ),
                        "obitos_abs": self.parse_number(
                            regiao["incidenca_obitos_doenca_respiratoria"]["obitos_doenca_respiratoria_abs"][i]
                        ),
                        "custo_internacao": self.parse_number(
                            regiao["incidenca_obitos_doenca_respiratoria"]["custo_internacao_doenca_respiratoria"][i]
                        ),
                        "obitos_infantil": self.parse_number(
                            regiao["incidenca_obitos_doenca_respiratoria"]["obitos_doenca_respiratoria_infantil"][i]
                        ),
                    })
                    
                    if len(fatos_bulk) >= self.BATCH_SIZE:
                        self.__insert_bulk("fato_socioeconomico", fatos_bulk)
                        fatos_bulk.clear()
                        
                    if len(internacoes_bulk) >= self.BATCH_SIZE:
                        self.__insert_bulk("internacoes", internacoes_bulk)
                        internacoes_bulk.clear()
                        
                    if len(coleta_bulk) >= self.BATCH_SIZE:
                        self.__insert_bulk("coleta_esgoto", coleta_bulk)
                        coleta_bulk.clear()
                        
                    if len(doencas_bulk) >= self.BATCH_SIZE:
                        self.__insert_bulk("obitos_doenca_respiratoria", doencas_bulk)
                        doencas_bulk.clear()
                        
                        
                self.__insert_bulk("fato_socioeconomico", fatos_bulk)
                self.__insert_bulk("internacoes", internacoes_bulk)
                self.__insert_bulk("coleta_esgoto", coleta_bulk)
                self.__insert_bulk("obitos_doenca_respiratoria", doencas_bulk)
                
            print(f"Importação do arquivo {file} finalizada com sucesso")

if __name__ == "__main__":
    importador = Import(os.path.join(os.path.dirname(__file__), "raw_data"))
    importador.init_connection(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY")
    )
    importador.import_to_supabase()
