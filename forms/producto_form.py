class ProductoForm:
    def __init__(self, nombre='', precio='', cantidad=''):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.errors = {}

    def validate(self):
        if not self.nombre:
            self.errors['nombre'] = 'El nombre es requerido'
        if not self.precio:
            self.errors['precio'] = 'El precio es requerido'
        if not self.cantidad:
            self.errors['cantidad'] = 'La cantidad es requerida'
        return len(self.errors) == 0

class ClienteForm:
    def __init__(self, nombre='', email='', telefono='', direccion=''):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.errors = {}

    def validate(self):
        if not self.nombre:
            self.errors['nombre'] = 'El nombre es requerido'
        if not self.email:
            self.errors['email'] = 'El email es requerido'
        return len(self.errors) == 0