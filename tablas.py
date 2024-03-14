import sqlite3
import json
import hashlib as hash
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

