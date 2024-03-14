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

    # Crear dataframes a partir de las consultas
    df_users = pd.read_sql_query(q_users, con)
    df_admins = pd.read_sql_query(q_admins, con)

    # Ajustar el formato de las fechas de string a datatime
    df_users['fecha'] = pd.to_datetime(df_users['fecha'], format="%d/%m/%Y")
    df_admins['fecha'] = pd.to_datetime(df_admins['fecha'], format="%d/%m/%Y")

    # Ordenar los dataframes segun el nombre de usuario y la fecha
    df_users = df_users.sort_values(by=['user_id', 'fecha'])
    df_admins = df_admins.sort_values(by=['user_id', 'fecha'])

    # Crear la columna diferencia en los dataframes con la diferencia de dias desde el cambio anterior
    df_users['diferencia'] = pd.to_numeric(df_users.groupby('user_id')['fecha'].diff().dt.days)
    df_admins['diferencia'] = pd.to_numeric(df_admins.groupby('user_id')['fecha'].diff().dt.days)

    # Hacer la media de las diferencias en cada usuario
    media_users = df_users.groupby('user_id')['diferencia'].mean().reset_index()
    media_admins = df_admins.groupby('user_id')['diferencia'].mean().reset_index()

    # Imprimir por pantalla los tiempos medios por usuario
    print("Tiempo medio trascurrido en días para usuarios normales: ")
    print(media_users)
    print("Tiempo medio trascurrido en días para usuarios admin: ")
    print(media_admins)

    # Crear los gráficos
    plt.figure(figsize=(12, 6))
    plt.subplots_adjust(hspace=0.5)

    # Grafico para usuarios normales
    plt.subplot(1, 2, 1)
    plt.title('Tiempo medio trascurrido en días para usuarios normales')
    plt.bar(media_users['user_id'], media_users['diferencia'], color='black')
    plt.xlabel('Nombre de Usuario')
    plt.ylabel('Tiempo Medio (días)')
    plt.xticks(rotation=90)

    # Gráfico para usuarios administradores
    plt.subplot(1, 2, 2)
    plt.title('Tiempo medio transcurrido en días para usuarios admin')
    plt.bar(media_admins['user_id'], media_admins['diferencia'], color='black')
    plt.xlabel('Nombre de Usuario')
    plt.ylabel('Tiempo Medio (días)')
    plt.xticks(rotation=90)

    # Ajustar el espacio entre los gráficos
    plt.tight_layout()

    # Mostrar los gráficos
    plt.show()

def ej4_2():
    


