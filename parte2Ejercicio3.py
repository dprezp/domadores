import requests



url = 'https://cve.circl.lu/api/last/10'
response = requests.get(url)
data = response.json()
sol ={
    'CVE':[],
    'Descripcion':[],
    'Fecha':[]
}

for vulnerabilidad in data:
    cve = vulnerabilidad.get('id')
    descripción = vulnerabilidad.get('summary')
    fecha = vulnerabilidad.get('Published')
    sol['CVE'].append(cve)
    sol['Descripcion'].append(descripción)
    sol['Fecha'].append(fecha)

