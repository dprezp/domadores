import sqlite3
import json
import hashlib as hash

import pandas as pd


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


# Para saber si el usuario tiene una contraseña segura o no
# (que aparezca enla lista de contraseñas comunes)
def esSegura(contrasena, hash):
    for hashes in hash:
        if contrasena == hashes:
            return False
    return True


# Hashea las contraseñas más comunes
def hashear():
    hashes = []
    comunes = open('data/comunes.txt', 'r')
    for comun in comunes:
        hashComun = hash.md5(comun[:-1].encode(encoding="utf-8")).hexdigest()
        # Todo menos el ultimo caracter para evitar el salto de linea
        hashes.append(hashComun)
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

        hashesInseguros = hashear()

        for elem in datos["usuarios"]:
            clave = list(elem.keys())[0]

            # Para saber si el usuario tiene una contraseña segura o no
            seguridad = 0
            if esSegura(elem[clave]['contrasena'], hashesInseguros):
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

def consultas():

    #CONSULTAS EJ 2
    #conexion a la base de datos
    con = sqlite3.connect('datos.db')

    #Hacemos las consultas para sacar los dataFrames
    q_users = "SELECT * FROM usuarios"
    q_fechas = "SELECT * FROM fechas_ips WHERE user_id IN(SELECT id FROM usuarios)"
    q_admin = "SELECT * FROM usuarios WHERE permisos IS 1"

    #sacamos los dataFrames
    df_users = pd.read_sql_query(q_users, con)
    df_fechas = pd.read_sql_query(q_fechas, con)
    df_admins = pd.read_sql_query(q_admin,con)


    #Numero de muestras
    print("Número de muestras de usuarios:", end ="")
    print(df_users['id'].count(),end ="\n")
    print("Número de muestras de fechas_ips:", end ="")
    print(df_fechas['id'].count(),end="\n")

    #Media y desviación estándar del total de fecahs en las que se ha cambiado la contraseña
    print("Media y desviación estándar del total de fechas en las que se ha cambiado la contraseña")
    print("Media:",end="")
    print(df_fechas.groupby('user_id').count().mean()['fecha'])
    print("Desviación estandar",end="")
    print(df_fechas.groupby('user_id').count().std()['fecha'])

    #Media y desviacón estándar del total de IPS que se han detectado
    print("Media y desviacón estándar del total de IPS que se han detectado")
    print("Media:",end="")
    print(df_fechas.groupby('user_id').count().mean()['ip'])
    print("Desviación estandar", end="")
    print(df_fechas.groupby('user_id').count().std()['ip'])

    #Media y desviación estándar del número de emails recibidos de phishing en los que ha interactuado cualquier usuario
    print("Media y desviación estándar del número de emails recibidos de phishing en los que ha interactuado cualquier usuario")
    print("Media:", end="")
    print(df_users['emails_phishing'].mean())
    print("Desviación estandar", end="")
    print(df_users['emails_phishing'].std())

    #Valor mínimo y valor máximo del total de emails recibidos
    print("Valor mínimo y valor máximo del total de emails recibidos")
    print("Máximo:",end="")
    print(df_users['emails_totales'].max())
    print("Mínimo:",end="")
    print(df_users['emails_totales'].min())

    #Valor mínimo y valor máximo del número de emails phishing en los que ha interactuado un administrador
    print("Valor mínimo y valor máximo del número de emails phishing en los que ha interactuado un administrador")
    print("Máximo:", end="")
    print(df_admins['emails_clickados'].max())
    print("Mínimo:", end="")
    print(df_admins['emails_clickados'].min())

    con.close()

