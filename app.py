#from flask import Flask
import json
import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt


import tablas
import ejercicio4


if os.path.exists('datos.db'):
        os.remove('datos.db')

tablas.crearLegal()
tablas.crearUsers()

#ejercicio4.ej4_1()
#ejercicio4.ej4_2()
ejercicio4.ej4_3()
#ejercicio4.ej4_4()
#tablas.consultas2()
tablas.consultas3()
