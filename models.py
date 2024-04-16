from flask_login import UserMixin
import sqlite3
import hashlib


class User(UserMixin):
    def __init__(self, user_id, password, user_role):
        self.id = user_id
        self.password = password
        self.user_role = user_role

    def get_id(self):
        return self.id


    @staticmethod
    def get(user_id):
        # Aquí realizarías la consulta a la base de datos para obtener el usuario por su ID
        # Retorna el objeto User si se encuentra, o None si no existe
        con = sqlite3.connect('datos.db')
        cur = con.cursor()
        cur.execute("SELECT id, contrasena, user_role FROM usuarios WHERE id=?", (user_id,))
        user_data = cur.fetchone()
        con.close()
        if user_data:
            return User(*user_data)
        return None

    def is_admin(self):
        return self.user_role == 'admin'

    @staticmethod
    def find_by_tlf(tlf):
        # Aquí realizarías la consulta a la base de datos para encontrar un usuario por su nombre de usuario
        # Retorna el objeto User si se encuentra, o None si no existe
        con = sqlite3.connect('datos.db')
        cur = con.cursor()
        cur.execute("SELECT id, contrasena, user_role FROM usuarios WHERE telefono=?", (tlf,))
        user_data = cur.fetchone()
        con.close()
        if user_data:
            return User(*user_data)
        return None

    def check_password(self, password):
        hashed_pass = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
        return hashed_pass == self.password
