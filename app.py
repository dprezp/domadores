from flask import Flask
import json
import sqlite3
import os
import pandas as pd

if os.path.exists('datos.db'):
        os.remove('datos.db')

with open('data/legal_data_online.json', 'r') as f:
    datos = json.load(f)
    con = sqlite3.connect('datos.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS legal("
                "id TEXT PRIMARY KEY,"
                "cookies INTEGER,"
                "aviso INTEGER,"
                "proteccion_de_datos INTEGER,"
                "creacion INTEGER"
                ");")
    con.commit()

    claves = datos["legal"][0].keys
    for elem in datos["legal"]:
        clave = list(elem.keys())[0]
        print(clave)
        print(elem[clave]["cookies"])

        cur.execute("INSERT OR IGNORE INTO legal (id, cookies, aviso, proteccion_de_datos, creacion)"\
                    "VALUES ('%s','%d','%d','%d','%d')" %
                    (clave, int(elem[clave]['cookies']), int(elem[clave]['aviso']), int(elem[clave]['proteccion_de_datos']), int(elem[clave]['creacion'])))
        con.commit()
    """
    select_query = 'SELECT * FROM legal;'
    df = pd.read_sql_query(select_query, con)
    print(df)
    """

    # app.run()

with open('data/users_data_online.json', 'r') as f:
    datos = json.load(f)
    cur.execute("CREATE TABLE IF NOT EXISTS usuarios("
                "id TEXT PRIMARY KEY,"
                "telefono INTEGER,"
                "contrasena TEXT,"
                "provincia TEXT,"
                "permisos TEXT,"
                "emails_totales TEXT,"
                "emails_phising TEXT,"
                "emails_clickados TEXT"
                ");")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS fechas("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "fecha TEXT,"
                "user_id TEXT,"
                "FOREIGN KEY (user_id) REFERENCES usuarios(id)"
                ");")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS ips("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "ip TEXT,"
                "user_id TEXT,"
                "FOREIGN KEY (user_id) REFERENCES usuarios(id)"
                ");")
    con.commit()

    nclaves = datos["usuarios"][0].keys

    for elem in datos["usuarios"]:
        clave = list(elem.keys())[0]

        cur.execute("INSERT OR IGNORE INTO usuarios (id, telefono, contrasena, provincia, permisos, emails_totales, emails_phising, emails_clickados)" \
                    "VALUES ('%s','%s','%s','%s','%s', '%d', '%d', '%d')" %
                    (clave,elem[clave]['telefono'], elem[clave]['contrasena'],
                     elem[clave]['provincia'], elem[clave]['permisos'], int(elem[clave]['emails']['total']), int(elem[clave]['emails']['phishing']), int(elem[clave]['emails']['cliclados'])))
        con.commit()
        fechas = elem[clave]["fechas"]
        for fecha in fechas:
            cur.execute("INSERT OR IGNORE INTO fechas (user_id, fecha)" \
                        "VALUES ('%s', '%s')" %
                        (clave, fecha))
            con.commit()
        ips = elem[clave]["ips"]
        for ip in ips:
            cur.execute("INSERT OR IGNORE INTO ips (ip, user_id)" \
                        "VALUES ('%s', '%s')" %
                        (ip, clave))

    con.close()

