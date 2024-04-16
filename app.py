from flask import Flask, render_template, request, redirect, url_for, flash, abort
import ejercicio3
import ejercicio4
import parte2Ejercicio3
import tablas
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


tablas.init()


# Fundamental: pasamos el valor clave-valor de los mapas con **map
# Esto es gracias a que hemos puesto el mismo nombre para los valores en el html que los nombres de las claves del mapa.
# Para poder representar los gráficos, hemos tenido que pasarlos a base64 y decodificar en el HTML.
# Hemos tocado un poco de Bootstrap para darle un toque estilístico sutil.


@app.route('/')
def basic():  # pagina de inicio
    return render_template('home.html')


@app.route('/ejercicio4')
def ej4():  # pagina de inicio del ejercicio 4
    return render_template('ejercicio4.html')


@app.route('/ejercicio2')
@login_required
def ej2():
    data2 = tablas.consultas2()
    return render_template('ejercicio2.html', **data2)


@app.route('/ejercicio3')
@login_required
def ej3():
    data3 = ejercicio3.consultas()
    print(data3)
    return render_template('ejercicio3.html', **data3)


@app.route('/parte1')
@login_required
def ej4_1():
    data4_1 = ejercicio4.ej4_1()
    return render_template('4parte1.html', **data4_1)


@app.route('/parte2', methods=['GET', 'POST'])
@login_required
def ej4_2():
    if request.method == 'POST':
        usuarios = request.form['num_usuarios']
        if not usuarios:
            data4_2 = {'df_inseguro': None}
        else:
            usuarios = int(usuarios)
            if usuarios <= 0:
                data4_2 = {'df_inseguro': None}
            else:
                if 'clicks_filter' in request.form:
                    clicks_filter = request.form['clicks_filter']
                    if clicks_filter == 'mas50':
                        data4_2 = ejercicio4.ej4_2(usuarios, '+')
                    elif clicks_filter == 'menos50':
                        data4_2 = ejercicio4.ej4_2(usuarios, '-')
                    else:
                        data4_2 = ejercicio4.ej4_2(usuarios, None)
    else:
        data4_2 = {'df_inseguro': None}
    return render_template('4parte2.html', **data4_2)


@app.route('/parte3')
@login_required
def ej4_3():
    data4_3 = ejercicio4.ej4_3()
    return render_template('4parte3.html', **data4_3)


@app.route('/parte4')
@login_required
def ej4_4():
    data4_4 = ejercicio4.ej4_4()
    return render_template('4parte4.html', **data4_4)


@app.route('/Ej3parte2')
@login_required
def ej3_2():
    data3_2 = parte2Ejercicio3.parte2Ej3()
    return render_template('3parte2.html', **data3_2)


@app.route('/parte1-2', methods=["GET", "POST"])
@login_required
def ej1_2():
    if request.method == 'POST':
        webs = int(request.form['num_webs'])
        if webs <= 0:
            data1_2 = {'html_data': None}
        else:
            data1_2 = ejercicio4.part2_ej1_2(webs)
    else:
        data1_2 = {'html_data': None}

    return render_template('parte2ejercicio1-2.html', **data1_2)


###### LOGIN


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get(username)
        # jose.suarez --> password
        if user and user.check_password(password):
            login_user(user)
            return redirect("/")
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_authenticated or not current_user.is_admin():
        abort(403)  # Prohibido
    # Si el usuario es administrador, muestra el dashboard del admin
    return render_template('admin.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/login")




if __name__ == '__main__':
    app.run(debug=True)
