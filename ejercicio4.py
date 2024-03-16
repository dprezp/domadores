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
    con = sqlite3.connect('datos.db')

    q_inseguro = ("SELECT id, emails_clickados, emails_phishing  "
                  "FROM usuarios WHERE segura IS 0 AND emails_clickados IS NOT 0 "
                  "AND emails_phishing IS NOT 0 ;")

    df_inseguro = pd.read_sql_query(q_inseguro, con)

    # Calcular probabilidad de éxito para ataques de phishing
    df_inseguro['probabilidad'] = df_inseguro['emails_clickados'] / df_inseguro['emails_phishing'] * 100
    df_inseguro.sort_values(by='probabilidad', ascending=False, inplace=True)

    # Seleccionar los primeros 10 usuarios con más probabilidad
    df_inseguro = df_inseguro.head(10)

    # Imprimirlos por pantalla
    print(df_inseguro)

    # Crear el grafico de probabilidad por usuario
    df_inseguro.plot(kind='bar', x='id', y='probabilidad', color='black')
    plt.title("Usuarios más criticos")
    plt.xlabel("Usuario")
    plt.ylabel("Probabilidad de clickar un correo spam (%)")
    plt.xticks(rotation=45, ha='right')  # Rotar los nombres de usuario para mayor legibilidad
    plt.tight_layout()
    plt.show()

    con.close()


def ej4_3():
    #conectamos la base de datos
    con = sqlite3.connect('datos.db')

    #Se realiza la consulta y se saca el dataframe
    q_webs='SELECT id, cookies, aviso, proteccion_de_datos FROM legal;'
    df_webs = pd.read_sql_query(q_webs, con)

    #Se calcula la cantidad de políticas deprecated
    df_webs['deprecated'] = df_webs[['cookies','aviso','proteccion_de_datos']].apply(lambda row: sum(row==0), axis=1)

    # ordenar las webs según deprecated (cogemos 5 primeros)
    df_webs.sort_values(by=['deprecated'], inplace=True, ascending=False)
    first_five = df_webs.head(5)

    #nombre de la gráfica
    df_webs = df_webs.set_index('id')
    print(df_webs)

    #crear gráfico de barras correspondientes
    first_five.plot(kind='bar')
    plt.title('politicas desactualizadas')
    plt.xlabel('Página web')
    plt.ylabel('estado')
    plt.legend()
    plt.tight_layout()
    plt.show()
    #cerrar base de datos
    con.close()

def ej4_4():
    con = sqlite3.connect('datos.db')

    #Se realiza la consulta y se saca el dataframe como en el ejercicio anterior
    q_webs='SELECT id, cookies, aviso, proteccion_de_datos, creacion FROM legal;'
    df_webs = pd.read_sql_query(q_webs, con)

    #Creamos un distintivo de politicas de seguridad
    df_webs['dist'] = (df_webs['proteccion_de_datos'] == 1) & (df_webs['aviso'] == 1) & (df_webs['cookies'] == 1)

    #lo ordenamos por año de creación y con el distintivo
    df_webs_ordenado = df_webs.groupby(['creacion','dist']).size().unstack()
    print(df_webs_ordenado)

    #Sacamos el gráfico
    df_webs_ordenado.plot(kind='bar')
    plt.title('Web que cumplen todas las politicas de seguridad ordenadas en años ')
    plt.xlabel('Creación')
    plt.ylabel('cantidad de webs')
    plt.legend(['No cumplen', 'Si cumplen'])
    plt.tight_layout()
    plt.show()
    con.close()



