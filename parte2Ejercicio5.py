import sqlite3
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from subprocess import call
import graphviz



def ej5():
    conn = sqlite3.connect('datos.db')

    # Petición a la BD
    query = "SELECT id, segura, permisos, emails_totales, emails_phishing, emails_clickados, critico FROM usuarios"

    # Creamos los dataframes
    df_BD = pd.read_sql_query(query, conn)

    df_BD['tasa_phishing'] = np.where(df_BD['emails_totales'] != 0, df_BD['emails_phishing'] / df_BD['emails_totales'],
                                      0)
    df_BD['tasa_clicados'] = np.where(df_BD['emails_phishing'] != 0,
                                      df_BD['emails_clickados'] / df_BD['emails_phishing'], 0)
    df_BD['permisos_seguros'] = (df_BD['permisos'] == 1) & (df_BD['segura'] == 0)

    x = df_BD[['tasa_phishing', 'tasa_clicados', 'permisos_seguros']]
    y = df_BD['critico']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Eliminar filas con NaN en x_train y y_train
    x_train = x_train.dropna()
    y_train = y_train[x_train.index]

    # Dividir los datos en conjuntos de entrenamiento y prueba
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

    # entrenamos modelos
    # Árbol de Decisión
    tree_model = DecisionTreeClassifier()
    tree_model = tree_model.fit(x_train, y_train)

    # Random Forest
    forest_model = RandomForestClassifier()
    forest_model = forest_model.fit(x_train, y_train)

    # Evaluamos el rendimiento de los modelos
    y_pred = tree_model.predict(x_test)
    tree_score = accuracy_score(y_test, y_pred)
    y_pred = forest_model.predict(x_test)
    forest_score = accuracy_score(y_test, y_pred)

    #Regresion lineal
    x_regresion = x_train['permisos_seguros'] + x_train['tasa_clicados']
    x_regresion = x_regresion.values.reshape(-1, 1)
    linear_model = LinearRegression()
    linear_model = linear_model.fit(x_regresion, y_train)
    x_test_regresion = x_test['permisos_seguros'] + x_test['tasa_clicados']
    x_test_regresion = x_test_regresion.values.reshape(-1,1)
    y_pred = linear_model.predict(x_test_regresion)
    y_pred = np.round(y_pred)
    lineal_score = accuracy_score(y_test, y_pred)

    #Imagen regresión lineal
    sorted_indices = np.argsort(x_test_regresion.flatten())
    x_test_regresion_sorted = x_test_regresion[sorted_indices]
    y_pred_sorted = y_pred[sorted_indices]
    plt.scatter(x_test_regresion, y_test, color="black")
    plt.plot(x_test_regresion_sorted, np.round(y_pred_sorted), color="blue", linewidth=3)
    plt.xlabel('tasa de phishing')
    plt.ylabel('Critico')
    plt.title('Ajuste del modelo de regresión lineal en la variante tasa_phishing')
    plt.show()

    #Imagen Decision tree
    dot_data = export_graphviz(tree_model, out_file=None, feature_names=x.columns, class_names=['No critico', 'critico'])
    graph = graphviz.Source(dot_data)
    graph.render("critico", format ='png')

    #Imagen random forest
    for i in range(0,9):
       print(i)
       estimator = forest_model.estimators_[i]
       export_graphviz(estimator, out_file='tree.dot', feature_names=x.columns, class_names=['No critico', 'critico'])
       call(['dot', '-Tpng', 'tree.dot', '-o', 'tree' + str(i) + '.png', '-Gdpi=600'])



    sol = {
        'regresionLineal': linear_model,
        'randomForest': forest_model,
        'decisionTree': tree_model,
    }

    conn.close()

    return sol
