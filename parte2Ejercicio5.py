import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import json

conn = sqlite3.connect('datos.db')

#Petición a la BD
query = "SELECT id,segura, permisos, emails_totales, emails_phishing, emails_clickados, critico FROM usuarios"

#Creamos los dataframes
df_BD = pd.read_sql_query(query, conn)

df_BD['tasa_phishing'] = df_BD['emails_phishing'] / df_BD['emails_totales']
df_BD['tasa_clicados'] = df_BD['emails_clickados'] / df_BD['emails_phishing']
df_BD['permisos_seguros'] = (df_BD['permisos'] ==1) & (df_BD['segura'] ==0)

x = df_BD[['tasa_phishing','tasa_clicados','permisos_seguros']]
y = df_BD['critico']

# Dividir los datos en conjuntos de entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#entrenamos modelos
#Regresión logistica
logistic_model = LogisticRegression()
logistic_model.fit(x_train, y_train)

# Árbol de Decisión
tree_model = DecisionTreeClassifier()
tree_model.fit(x_train, y_train)

#Random Forest
forest_model = RandomForestClassifier()
forest_model.fit(x_train, y_train)


#Evaluamos el rendimiento de los modelos
y_pred = tree_model.predict(x_test)
tree_score = accuracy_score(y_test, y_pred)
y_pred = forest_model.predict(x_test)
forest_score = accuracy_score(y_test, y_pred)
y_pred = logistic_model.predict(x_test)
logistic_score = accuracy_score(y_test, y_pred)

print("Accuracy:\n")
print("Regresion logistica: ", logistic_score)
print("Árbol de decisión: ", tree_score)
print("Random forest: ", forest_score)
conn.close()
