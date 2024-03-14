#from flask import Flask
import json
import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

import ejercicio4

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
    cur.execute("CREATE TABLE IF NOT EXISTS fechas_ips("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "fecha DATETIME,"
                "ip TEXT,"
                "user_id TEXT,"
                "FOREIGN KEY (user_id) REFERENCES usuarios(id)"
                ");")
    con.commit()

    con.commit()

    nclaves = datos["usuarios"][0].keys

    for elem in datos["usuarios"]:
        clave = list(elem.keys())[0]

        cur.execute("INSERT OR IGNORE INTO usuarios (id, telefono, contrasena, provincia, permisos, emails_totales, emails_phising, emails_clickados)" \
                    "VALUES ('%s','%s','%s','%s','%s', '%d', '%d', '%d')" %
                    (clave,elem[clave]['telefono'], elem[clave]['contrasena'],
                     elem[clave]['provincia'], elem[clave]['permisos'], int(elem[clave]['emails']['total']), int(elem[clave]['emails']['phishing']), int(elem[clave]['emails']['cliclados'])))
        con.commit()
        i = 0
        fechas = elem[clave]["fechas"]
        for fecha in fechas:
            cur.execute("INSERT OR IGNORE INTO fechas_ips (fecha, ip, user_id)" \
                        "VALUES ('%s', '%s', '%s')" %
                        (fecha, elem[clave]["ips"][i], clave))
            if elem[clave]["ips"] != "None":
                i += 1
            con.commit()

    con.close()

    con = sqlite3.connect('datos.db')

    q_users = ("SELECT * FROM fechas_ips "
               "WHERE user_id IN "
               "(SELECT id FROM usuarios WHERE permisos == '0');")

    q_admins = ("SELECT * FROM fechas_ips "
                "WHERE user_id IN "
                "(SELECT id FROM usuarios  WHERE permisos == '1');")

    df_users = pd.read_sql_query(q_users, con)
    df_admins = pd.read_sql_query(q_admins, con)

    df_users['fecha'] = pd.to_datetime(df_users['fecha'], format="%d/%m/%Y")
    df_admins['fecha'] = pd.to_datetime(df_admins['fecha'], format="%d/%m/%Y")

    # Ordenar los DataFrames segun el nombre de usuario y la fecha
    df_users = df_users.sort_values(by=['id', 'fecha'])
    df_admins = df_admins.sort_values(by=['id', 'fecha'])

    df_users['diferencia'] = pd.to_numeric(df_users.groupby('id')['fecha'].diff().dt.days)
    df_admins['diferencia'] = pd.to_numeric(df_admins.groupby('id')['fecha'].diff().dt.days)

    media_users = df_users.groupby('id')['diferencia'].mean()
    media_users['tiempo'] = df_users['diferencia']
    media_users.drop(['diferencia'])

    media_admins = df_admins.groupby('id')['diferencia'].mean()
    media_admins['tiempo'] = df_admins['diferencia']
    media_admins.drop(['diferencia'])

    print("Media de tiempo medio entre cambios de contraseña por usuario normal: " + media_users)
    print("Media de tiempo medio entre cambios de contraseña por usuario administrador: " + media_admins)

    plt.figure(figsize=(25, 16))

    plt.subplot(1, 2, 1)
    plt.title('Tiempo medio trascurrido en días ara usuarios normales')
    media_users.plot(kind='bar', x='user_id', y='tiempo', color='aqua')

    plt.subplot(1, 2, 2)
    plt.title('Tiempo medio trascurrido en días ara usuarios admin')
    media_admins.plot(kind='bar', x='user_id', y='tiempo', color='magenta')

    plt.show()


