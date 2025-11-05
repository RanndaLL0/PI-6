import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


conn = psycopg2.connect(
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    dbname=DBNAME,
    sslmode="require"
)
cur = conn.cursor()

anos = [str(y) for y in range(2010, 2024)]
for ano in anos:
    cur.execute("""INSERT INTO ano (ano) 
                   VALUES (%s) 
                   ON CONFLICT (ano) DO NOTHING""", (ano,))
conn.commit()

def parse_number(value):
    if value == "-" or value is None:
        return None
    value = value.replace(".", "").replace(",", ".")
    try:
        return int(float(value))
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return None

RAW_DIR = "raw_data"

for file in os.listdir(RAW_DIR):
    if not file.endswith(".json"):
        continue

    area = os.path.splitext(file)[0]
    print(f"Processando {area}...")

    cur.execute("INSERT INTO area (nome) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id;", (area,))
    area_id = cur.fetchone()[0] if cur.rowcount > 0 else None
    if not area_id:
        cur.execute("SELECT id FROM estado WHERE nome=%s", (area,))
        area_id = cur.fetchone()[0]

    data = json.load(open(os.path.join(RAW_DIR, file), encoding="utf-8"))

    for municipio in data:
        nome = municipio["regiao"]
        tipo = municipio["area"]
        area_val = parse_number(municipio["fato"]["area_do_municipio"][0])

        cur.execute("""
            INSERT INTO municipio (nome, area_id, area_km2, tipo_area)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (nome, area_id, area_val, tipo))
        municipio_id = cur.fetchone()[0]

        for i, ano in enumerate(municipio["data"]):
            cur.execute("SELECT id FROM ano WHERE ano=%s", (ano,))
            ano_id = cur.fetchone()[0]

            f = municipio["fato"]
            cur.execute("""
                INSERT INTO fato_socioeconomico (municipio_id, ano_id, populacao, moradias,
                    densidade_domiciliar, pib_absoluto, pib_per_capita, densidade_demografica)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
            """, (
                municipio_id, ano_id,
                parse_number(f["populacao"][i]),
                parse_number(f["moradias"][i]),
                parse_number(f["densidade_domiciliar"][i]),
                parse_number(f["pib_absoluto"][i]),
                parse_number(f["pib_per_capita"][i]),
                parse_number(f["densidade_demografica"][i])
            ))

            i_data = municipio["internacoes"]
            cur.execute("""
                INSERT INTO internacoes (municipio_id, ano_id, dengue, leptospirose, malaria, infantil, adolescencia)
                VALUES (%s,%s,%s,%s,%s,%s,%s);
            """, (
                municipio_id, ano_id,
                parse_number(i_data["internacao_dengue"][i]),
                parse_number(i_data["internacao_leptospirose"][i]),
                parse_number(i_data["internacao_malaria"][i]),
                parse_number(i_data["internacao_infantil"][i]),
                parse_number(i_data["internacao_adolecencia"][i])
            ))

            c_e = municipio["coleta_esgoto"]
            cur.execute("""
                INSERT INTO coleta_esgoto (municipio_id, ano_id, pop_sem_coleta, pop_urbana_com_coleta,
                    pop_urbana_sem_coleta, esgoto_coletado, esgoto_tratado)
                VALUES (%s,%s,%s,%s,%s,%s,%s);
            """, (
                municipio_id, ano_id,
                parse_number(c_e["populacao_sem_coleta_de_esgoto"][i]),
                parse_number(c_e["populacao_urbana_com_coleta"][i]),
                parse_number(c_e["populacao_urbana_sem_coleta"][i]),
                parse_number(c_e["esgoto_coletado"][i]),
                parse_number(c_e["esgoto_tratado"][i])
            ))

            c_a = municipio["coleta_agua"]
            cur.execute("""
                INSERT INTO coleta_agua (municipio_id, ano_id, pop_com_acesso, pop_sem_acesso,
                    pop_urbana_com_acesso, pop_urbana_sem_acesso)
                VALUES (%s,%s,%s,%s,%s,%s);
            """, (
                municipio_id, ano_id,
                parse_number(c_a["populacao_com_acesso_a_agua"][i]),
                parse_number(c_a["populacao_sem_acesso_a_agua"][i]),
                parse_number(c_a["populacao_urbana_com_acesso_a_agua"][i]),
                parse_number(c_a["populacao_urbana_sem_acesso_a_agua"][i])
            ))

            o = municipio["incidenca_obitos_doenca_respiratoria"]
            cur.execute("""
                INSERT INTO obitos_doenca_respiratoria 
                    (municipio_id, ano_id, obitos_cem, obitos_abs,
                    custo_internacao, obitos_infantil)
                VALUES (%s,%s,%s,%s,%s,%s);
            """, (
                municipio_id, ano_id,
                parse_number(o["obitos_doenca_respiratoria_cem"][i]),
                parse_number(o["obitos_doenca_respiratoria_abs"][i]),
                parse_number(o["custo_internacao_doenca_respiratoria"][i]),
                parse_number(o["obitos_doenca_respiratoria_infantil"][i])
            ))

    conn.commit()

cur.close()
conn.close()