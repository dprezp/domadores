from flask import Flask, render_template
import ejercicio3
import tablas
# import ejercicio4


app = Flask(__name__)

tablas.init()


@app.route('/')
def basic():  # pagina de inicio
    return render_template('home.html')


@app.route('/ejercicio2')
def ej2():
    data2 = tablas.consultas2()
    return render_template('ejercicio2.html', **data2)


@app.route('/ejercicio3')
def ej3():
    data3 = ejercicio3.consultas()
    print(data3)
    return render_template('ejercicio3.html', **data3)


if __name__ == '__main__':
    app.run(debug=True)







