from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password, rol='usuario'):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password
        self.rol = rol

    def es_admin(self):
        return self.rol == 'admin'