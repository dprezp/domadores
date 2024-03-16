import sqlite3
import json
import hashlib as hash
import pandas as pd


def consultasUserTypeFilter():
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

    # Numero de apariciones de Phishing en ambos grupos
    print("El numero de apariciones de phishing en usuarios con permisos '0'")
    print("Apariciones: ", end='')
    print(df_users['emails_phishing'].sum())

    print("El numero de apariciones de phishing de usuarios con permisos '1'")
    print("Apariciones: ", end='')
    print(df_admin['emails_phishing'].sum())

    # Numero de valores ausentes de phishing en ambos grupos
    print("El numero de valores ausentes de phishing en usuarios con permisos '0'")
    print("Ausencias: ", end='')
    print(df_users['emails_phishing'].isnull().sum())

    print("El numero de valores ausentes de phishing de usuarios con permisos '1'")
    print("Ausencias: ", end='')
    print(df_admin['emails_phishing'].isnull().sum())

    # Mediana de phishing encontrado en los usuarios de ambos grupos
    print("La mediana de phishing en usuarios con permisos '0'")
    print("Mediana: ", end='')
    print(df_users['emails_phishing'].median())

    print("La mediana de phishing de usuarios con permisos '1'")
    print("Mediana: ", end='')
    print(df_admin['emails_phishing'].median())

    # Media de phishing encontrado en los usuarios de ambos grupos
    print("La media de phishing en usuarios con permisos '0'")
    print("Media: ", end='')
    print(round(df_users['emails_phishing'].mean(), 2))

    print("La media de phishing de usuarios con permisos '1'")
    print("Media: ", end='')
    print(round(df_admin['emails_phishing'].mean(), 2))

    # Varianza de phishing encontrado en los usuarios de ambos grupos
    print("La varianza de phishing en usuarios con permisos '0'")
    print("Varianza: ", end='')
    print(round(df_users['emails_phishing'].var(), 2))

    print("La varianza de phishing de usuarios con permisos '1'")
    print("Varianza: ", end='')
    print(round(df_admin['emails_phishing'].var(), 2))

    # Valor maximo de phishing encontrado en los usuarios de ambos grupos
    print("Valor maximo de phishing en usuarios con permisos '0'")
    print("Valor maximo: ", end='')
    print(df_users['emails_phishing'].max())

    print("Valor maximo de phishing de usuarios con permisos '1'")
    print("Valor maximo: ", end='')
    print(df_admin['emails_phishing'].max())

    # Valor minimo de phishing encontrado en los usuarios de ambos grupos
    print("Valor minimo de phishing en usuarios con permisos '0'")
    print("Valor minimo: ", end='')
    print(df_users['emails_phishing'].min())

    print("Valor minimo de phishing de usuarios con permisos '1'")
    print("Valor minimo: ", end='')
    print(df_admin['emails_phishing'].min())

    con.close()


def consultasPassFilter():

    # Concectamos a la base de datos
    con = sqlite3.connect('datos.db')

    # Ahora, agrupamos por usuarios con contraseñas debiles y fuertes. Las consulatas son las mismas


    # Creamos las consultas
    q_users_debil = "SELECT * FROM usuarios WHERE segura=0"
    q_users_fuerte = "SELECT * FROM usuarios WHERE segura=1"

    # Sacamos los dataFrames
    df_users_fuerte = pd.read_sql_query(q_users_fuerte, con)
    df_users_debil = pd.read_sql_query(q_users_debil, con)

    # Numero de apariciones de Phishing en ambos grupos
    print("Valores tomados para usuarios con contraseñas fuertes")

    print("Apariciones: ", end='')
    print(df_users_fuerte['emails_phishing'].sum())

    print("Ausencias: ", end='')
    print(df_users_fuerte['emails_phishing'].isnull().sum())

    print("Mediana: ", end='')
    print(df_users_fuerte['emails_phishing'].median())

    print("Media: ", end='')
    print(round(df_users_fuerte['emails_phishing'].mean(), 2))

    print("Varianza: ", end='')
    print(round(df_users_fuerte['emails_phishing'].var(), 2))

    print("Valor maximo: ", end='')
    print(df_users_fuerte['emails_phishing'].max())

    print("Valor minimo: ", end='')
    print(df_users_fuerte['emails_phishing'].min())

    print("------------------------------------------------")

    print("Valores tomados para usuarios con contraseñas débiles")

    print("Apariciones: ", end='')
    print(df_users_debil['emails_phishing'].sum())

    print("Ausencias: ", end='')
    print(df_users_debil['emails_phishing'].isnull().sum())

    print("Mediana: ", end='')
    print(df_users_debil['emails_phishing'].median())

    print("Media: ", end='')
    print(round(df_users_debil['emails_phishing'].mean(), 2))

    print("Varianza: ", end='')
    print(round(df_users_debil['emails_phishing'].var(), 2))

    print("Valor maximo: ", end='')
    print(df_users_debil['emails_phishing'].max())

    print("Valor minimo: ", end='')
    print(df_users_debil['emails_phishing'].min())

    con.close()
