import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64


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

    data = {}  # En este diccionario guardaremos lo que queramos meter en la pagina
    # En este caso seran los datos y los gráficos

    # Ajustar el formato de las fechas de string a datetime
    df_users['fecha'] = pd.to_datetime(df_users['fecha'], format="%d/%m/%Y")
    df_admins['fecha'] = pd.to_datetime(df_admins['fecha'], format="%d/%m/%Y")

    # Ordenar los dataframes segun el nombre de usuario y la fecha
    df_users = df_users.sort_values(by=['user_id', 'fecha'])
    df_admins = df_admins.sort_values(by=['user_id', 'fecha'])

    # Crear la columna diferencia en los dataframes con la diferencia de días desde el cambio anterior
    df_users['diferencia'] = pd.to_numeric(df_users.groupby('user_id')['fecha'].diff().dt.days)
    df_admins['diferencia'] = pd.to_numeric(df_admins.groupby('user_id')['fecha'].diff().dt.days)

    # Hacer la media de las diferencias en cada usuario
    media_users = df_users.groupby('user_id')['diferencia'].mean().reset_index()
    media_admins = df_admins.groupby('user_id')['diferencia'].mean().reset_index()

    # Generar los gráficos y convertirlos a base64
    fig_users = plt.figure(figsize=(12, 6))
    plt.bar(media_users['user_id'], media_users['diferencia'], color='black')
    plt.title('Tiempo medio trascurrido en días para usuarios normales')
    plt.xlabel('Nombre de Usuario')
    plt.ylabel('Tiempo Medio (días)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    buf_users = io.BytesIO()
    plt.savefig(buf_users, format='png')
    buf_users.seek(0)
    data_uri_users = base64.b64encode(buf_users.read()).decode('utf-8')
    plt.close(fig_users)

    fig_admins = plt.figure(figsize=(12, 6))
    plt.bar(media_admins['user_id'], media_admins['diferencia'], color='black')
    plt.title('Tiempo medio trascurrido en días para usuarios admin')
    plt.xlabel('Nombre de Usuario')
    plt.ylabel('Tiempo Medio (días)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    buf_admins = io.BytesIO()
    plt.savefig(buf_admins, format='png')
    buf_admins.seek(0)
    data_uri_admins = base64.b64encode(buf_admins.read()).decode('utf-8')
    plt.close(fig_admins)

    con.close()

    data["media_users"] = media_users
    data["media_admins"] = media_admins
    data["data_uri_users"] = data_uri_users
    data["data_uri_admins"] = data_uri_admins
    return data


def ej4_2(numUsers, mas):
    con = sqlite3.connect('datos.db')

    q_inseguro = ("SELECT id, emails_clickados, emails_phishing  "
                  "FROM usuarios WHERE segura IS 0 AND emails_clickados IS NOT 0 "
                  "AND emails_phishing IS NOT 0 ;")


    df_inseguro = pd.read_sql_query(q_inseguro, con)

    maxUsers = len(df_inseguro)
    if maxUsers < numUsers:
        return {'df_inseguro': None}

    # Calcular probabilidad de éxito para ataques de phishing
    df_inseguro['probabilidad'] = df_inseguro['emails_clickados'] / df_inseguro['emails_phishing'] * 100
    df_inseguro.sort_values(by='probabilidad', ascending=False, inplace=True)

    # Seleccionar los primeros X usuarios con más probabilidad
    df_inseguro = df_inseguro.head(numUsers)

    if mas is not None:
        if mas == '+':
            # Seleccionar los usuarios con más de 50% de probabilidad
            df_inseguro = df_inseguro[df_inseguro['probabilidad'] >= 50]
        if mas == '-':
            # Seleccionar los usuarios con menos de 50% de probabilidad
            df_inseguro = df_inseguro[df_inseguro['probabilidad'] < 50]

    # Generar el gráfico y convertirlo a base64
    plt.figure(figsize=(12, 6))
    plt.bar(df_inseguro['id'], df_inseguro['probabilidad'], color='black')
    plt.title("Usuarios más críticos")
    plt.xlabel("Usuario")
    plt.ylabel("Probabilidad de clickar un correo spam (%)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    data_uri = base64.b64encode(buf.read()).decode('utf-8') # pasamos el grafico a base64
    # Esto lo hacemos para que pueda ser pasado en un formato aceptable al html para luego mostrarlo
    plt.close()
    con.close()

    # Creamos un diccionario para poder enviarle a Flask los datos, con las mismas claves que las usadas en el html
    return {"data_uri": data_uri, "df_inseguro": df_inseguro}

def ej4_3():
    # Conectar con la base de datos
    con = sqlite3.connect('datos.db')

    # Realizar la consulta y obtener el dataframe
    q_webs = 'SELECT id, cookies, aviso, proteccion_de_datos FROM legal;'
    df_webs = pd.read_sql_query(q_webs, con)

    # Calcular la cantidad de políticas deprecated
    df_webs['deprecated'] = df_webs[['cookies', 'aviso', 'proteccion_de_datos']].apply(lambda row: sum(row == 0),
                                                                                       axis=1)

    # Ordenar las webs según deprecated y seleccionar las primeras cinco
    df_webs.sort_values(by=['deprecated'], inplace=True, ascending=False)
    first_five = df_webs.head(5)

    # Crear una representación HTML de los datos
    html_data = first_five.to_html()

    # Generar el gráfico y convertirlo a base64
    plt.figure(figsize=(12, 6))
    first_five.set_index('id').plot(kind='bar')
    plt.title('Políticas desactualizadas')
    plt.xlabel('Página web')
    plt.ylabel('Estado')
    plt.legend()
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    data_uri = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # Cerrar la conexión con la base de datos
    con.close()
    # Devolvemos un diccionario con la informacion que se mostrará en la pagina estatica
    return {"html_data": html_data, "data_uri": data_uri}


def ej4_4():
    # Conectar con la base de datos
    con = sqlite3.connect('datos.db')

    # Realizar la consulta y obtener el dataframe
    q_webs = 'SELECT id, cookies, aviso, proteccion_de_datos, creacion FROM legal;'
    df_webs = pd.read_sql_query(q_webs, con)

    # Crear un distintivo de políticas de seguridad
    df_webs['dist'] = (df_webs['proteccion_de_datos'] == 1) & (df_webs['aviso'] == 1) & (df_webs['cookies'] == 1)

    # Ordenar por año de creación y distintivo
    df_webs_ordenado = df_webs.groupby(['creacion', 'dist']).size().unstack()

    # Generar el gráfico y convertirlo a base64
    plt.figure(figsize=(12, 6))
    df_webs_ordenado.plot(kind='bar')
    plt.title('Webs que cumplen todas las políticas de seguridad ordenadas por años')
    plt.xlabel('Creación')
    plt.ylabel('Cantidad de webs')
    plt.legend(['No cumplen', 'Sí cumplen'])
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    data_uri = base64.b64encode(buf.read()).decode('utf-8') # Pasamos el gráfico a base64
    # para posteriormente mostrarlo en el html estatico
    plt.close()

    # Cerrar la conexión con la base de datos
    con.close()
    return {"data_uri": data_uri}  # devolvemos un diccionario que contiene el grafico en base64 (mostrado en el html)

def part2_ej1_2(num_pages):
    # Conectar con la base de datos
    con = sqlite3.connect('datos.db')

    # Realizar la consulta y obtener el dataframe
    q_webs = 'SELECT id, cookies, aviso, proteccion_de_datos, creacion FROM legal;'
    df_webs = pd.read_sql_query(q_webs, con)

    maxWebs = len(df_webs)

    if maxWebs < num_pages:
        return {'html_data': None}

    # Calcular la cantidad de políticas deprecated
    df_webs['deprecated'] = df_webs[['cookies', 'aviso', 'proteccion_de_datos']].apply(lambda row: sum(row == 0),
                                                                                       axis=1)

    # Ordenar las webs según deprecated y seleccionar las primeras cinco
    df_webs.sort_values(by=['deprecated', 'creacion'], inplace=True, ascending=[False, True])
    pages = df_webs.head(num_pages)

    # Crear una representación HTML de los datos
    html_data = pages.to_html()

    # Generar el gráfico y convertirlo a base64
    plt.figure(figsize=(12, 6))
    pages.set_index('id').plot(kind='bar')
    plt.title('Políticas desactualizadas')
    plt.xlabel('Página web')
    plt.ylabel('Estado')
    plt.legend()
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    data_uri = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # Cerrar la conexión con la base de datos
    con.close()
    # Devolvemos un diccionario con la informacion que se mostrará en la pagina estatica
    return {"html_data": html_data, "data_uri": data_uri}



