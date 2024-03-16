import sqlite3
import json
import hashlib as hash
import os
import pandas as pd


def init():
    if os.path.exists('datos.db'):
        os.remove('datos.db')

    crearLegal()
    crearUsers()


def crearLegal():
    with open('data/legal_data_online.json', 'r') as f:
        datos = json.load(f)
        con = sqlite3.connect('datos.db')
        cur = con.cursor()

        cur.execute("DROP TABLE IF EXISTS legal;")

        cur.execute("CREATE TABLE IF NOT EXISTS legal("
                    "id TEXT PRIMARY KEY,"
                    "cookies INTEGER,"
                    "aviso INTEGER,"
                    "proteccion_de_datos INTEGER,"
                    "creacion INTEGER"
                    ");")
        con.commit()

        for elem in datos["legal"]:
            clave = list(elem.keys())[0]
            cur.execute("INSERT OR IGNORE INTO legal (id, cookies, aviso, proteccion_de_datos, creacion)" \
                        "VALUES ('%s','%d','%d','%d','%d')" %
                        (clave, int(elem[clave]['cookies']), int(elem[clave]['aviso']),
                         int(elem[clave]['proteccion_de_datos']), int(elem[clave]['creacion'])))
            con.commit()
    con.close()


# Hashea las contraseñas más comunes en el diccionario SmallRockyou
def hashComunes():
    hashes = set()  # Meteremos los hash en un set, dado que comprobar si un hash pertenece al conjunto
    # Implica una complejidad O(1)
    with open('data/Smallrockyou.txt', 'r') as comunes:
        for comun in comunes:
            hashComun = hash.md5(comun[:-1].encode(encoding="utf-8")).hexdigest()
            # Evitamos incluir el salto de línea, porque el resultado del hash sería erróneo
            hashes.add(hashComun)
    return hashes


def crearUsers():
    with open('data/users_data_online.json', 'r') as f:
        datos = json.load(f)
        con = sqlite3.connect('datos.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS usuarios("
                    "id TEXT PRIMARY KEY,"
                    "telefono INTEGER,"
                    "contrasena TEXT,"
                    "segura INTEGER,"
                    "provincia TEXT,"
                    "permisos TEXT,"
                    "emails_totales INTEGER,"
                    "emails_phishing INTEGER,"
                    "emails_clickados INTEGER"
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

        hashesInseguros = hashComunes()

        for elem in datos["usuarios"]:
            clave = list(elem.keys())[0]

            # Para saber si el usuario tiene una contraseña segura o no
            seguridad = 0
            if elem[clave]['contrasena'] not in hashesInseguros: # Si no esta en el set de hashes inseguros, es segura
                seguridad = 1

            cur.execute(
                "INSERT OR IGNORE INTO usuarios (id, telefono, contrasena, segura, provincia, permisos, emails_totales, emails_phishing, emails_clickados)" \
                "VALUES ('%s','%s','%s', '%d','%s','%s', '%d', '%d', '%d')" %
                (clave, elem[clave]['telefono'], elem[clave]['contrasena'], seguridad,
                 elem[clave]['provincia'], elem[clave]['permisos'], int(elem[clave]['emails']['total']),
                 int(elem[clave]['emails']['phishing']), int(elem[clave]['emails']['cliclados'])))
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


def consultas2():

    # CONSULTAS EJ 2
    # conexion a la base de datos
    con = sqlite3.connect('datos.db')

    # Hacemos las consultas para sacar los dataFrames
    q_users = "SELECT * FROM usuarios"
    q_fechas = "SELECT * FROM fechas_ips WHERE user_id IN(SELECT id FROM usuarios)"
    q_admin = "SELECT * FROM usuarios WHERE permisos IS 1"

    # sacamos los dataFrames
    df_users = pd.read_sql_query(q_users, con)
    df_fechas = pd.read_sql_query(q_fechas, con)
    df_admins = pd.read_sql_query(q_admin,con)

    data = {}  # podriamos hacerlo de golpe, pero asi queda mas visual y sencillo de entender

    # Numero de muestras
    data["muestras_users"] = df_users['id'].count()
    data["muestras_fechas"] = df_fechas['id'].count()

    # Media y desviación estándar del total de fecahs en las que se ha cambiado la contraseña
    data["media_fechas"] = df_fechas.groupby('user_id').count().mean()['fecha']
    data["desviacion_fechas"] = df_fechas.groupby('user_id').count().std()['fecha']

    # Media y desviacón estándar del total de IPS que se han detectado
    data["media_ips"] = df_fechas.groupby('user_id').count().mean()['ip']
    data["desviacion_ips"] = df_fechas.groupby('user_id').count().std()['ip']

    # Media y desviación estándar del número de emails recibidos de phishing en los interactuo cualquier usuario
    data["media_phishing"] = df_users['emails_phishing'].mean()
    data["desviacion_phishing"] = df_users['emails_phishing'].std()

    # Valor mínimo y valor máximo del total de emails recibidos
    data["max_email"] = df_users['emails_totales'].max()
    data["min_email"] = df_users['emails_totales'].min()

    # Valor mínimo y valor máximo del número de emails phishing en los que ha interactuado un administrador
    data["max_phishing_admin"] = df_admins['emails_clickados'].max()
    data["min_phishing_admin"] = df_admins['emails_clickados'].min()
    con.close()
    return data



