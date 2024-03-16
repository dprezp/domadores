import sqlite3
import json
import hashlib as hash
import pandas as pd


def consultas():
    # CONSULTAS EJ 3
    # conexion a la base de datos
    con = sqlite3.connect('datos.db')

    # Hacemos las consultas para sacar los dataFrames
    # separamos por grupos en funcion de los permisos
    q_users = "SELECT * FROM usuarios WHERE permisos = '0'"
    q_admin = "SELECT * FROM usuarios WHERE permisos = '1'"

    # Sacamos los dataFrames
    df_users = pd.read_sql_query(q_users, con)
    df_admin = pd.read_sql_query(q_admin, con)

    # Ahora, agrupamos por usuarios con contraseñas debiles y fuertes. Las consulatas son las mismas

    # Creamos las consultas
    q_users_debil = "SELECT * FROM usuarios WHERE segura=0"
    q_users_fuerte = "SELECT * FROM usuarios WHERE segura=1"

    # Sacamos los dataFrames
    df_users_fuerte = pd.read_sql_query(q_users_fuerte, con)
    df_users_debil = pd.read_sql_query(q_users_debil, con)

    data = {}

    # Numero de apariciones de Phishing en ambos grupos
    data["phishing_users"] = df_users['emails_phishing'].sum()
    data["phishing_admin"] = df_admin['emails_phishing'].sum()

    # Numero de valores ausentes de phishing en ambos grupos
    data["ausencia_users"] = df_users['emails_phishing'].isnull().sum()
    data["ausencia_admin"] = df_admin['emails_phishing'].isnull().sum()

    # Mediana de phishing encontrado en los usuarios de ambos grupos
    data["mediana_users"] = df_users['emails_phishing'].median()
    data["mediana_admin"] = df_admin['emails_phishing'].median()

    # Media de phishing encontrado en los usuarios de ambos grupos
    data["media_users"] = round(df_users['emails_phishing'].mean(), 2)
    data["media_admin"] = round(df_admin['emails_phishing'].mean(), 2)

    # Varianza de phishing encontrado en los usuarios de ambos grupos
    data["varianza_users"] = round(df_users['emails_phishing'].var(), 2)
    data["varianza_admin"] = round(df_admin['emails_phishing'].var(), 2)

    # Valor maximo de phishing encontrado en los usuarios de ambos grupos
    data["max_users"] = df_users['emails_phishing'].max()
    data["max_admin"] = df_admin['emails_phishing'].max()

    # Valor minimo de phishing encontrado en los usuarios de ambos grupos
    data["min_users"] = df_users['emails_phishing'].min()
    data["min_admin"] = df_admin['emails_phishing'].min()

    # Usuarios con contraseña fuerte (replicacion de lo hecho anteriormente)

    data["phishing_fuerte"] = df_users_fuerte['emails_phishing'].sum()
    data["ausencia_fuerte"] = df_users_fuerte['emails_phishing'].isnull().sum()
    data["mediana_fuerte"] = df_users_fuerte['emails_phishing'].median()
    data["media_fuerte"] = round(df_users_fuerte['emails_phishing'].mean(), 2)
    data["varianza_fuerte"] = round(df_users_fuerte['emails_phishing'].var(), 2)
    data["max_fuerte"] = df_users_fuerte['emails_phishing'].max()
    data["min_fuerte"] = df_users_fuerte['emails_phishing'].min()

    # Usuarios con contraseña debil

    data["phishing_debil"] = df_users_debil['emails_phishing'].sum()
    data["ausencia_debil"] = df_users_debil['emails_phishing'].isnull().sum()
    data["mediana_debil"] = df_users_debil['emails_phishing'].median()
    data["media_debil"] = round(df_users_debil['emails_phishing'].mean(), 2)
    data["varianza_debil"] = round(df_users_debil['emails_phishing'].var(), 2)
    data["max_debil"] = df_users_debil['emails_phishing'].max()
    data["min_debil"] = df_users_debil['emails_phishing'].min()

    con.close()
    return data
