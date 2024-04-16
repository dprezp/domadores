import requests


def ej4API():
    url = 'https://haveibeenpwned.com/api/v3/breaches?IsSpamList=true'
    response = requests.get(url)
    data = response.json()
    sol ={
        'Nombre':[],
        'Descripcion':[],
        'Fecha':[]
    }

    for spam in data:
        titulo = spam.get('Title')
        descripcion = spam.get('Description')
        fecha = spam.get('AddedDate')
        sol['Nombre'].append(titulo)
        sol['Descripcion'].append(descripcion)
        sol['Fecha'].append(fecha)

    return sol


