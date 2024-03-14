import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def ej4_1():
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
    media_users.plot(kind='bar', x='user_id', y='', color='aqua')

    plt.subplot(1, 2, 2)
    plt.title('Tiempo medio trascurrido en días ara usuarios admin')
    media_admins.plot(kind='bar', x='user_id', y='Tiempo medio trascurrido', color='magenta')

    plt.show()


