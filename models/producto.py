class Producto:
    def __init__(self, id, nombre, precio, cantidad):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

class Cliente:
    def __init__(self, id_cliente, nombre, email, telefono, direccion):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion

class Pedido:
    def __init__(self, id_pedido, id_cliente, id_producto, cantidad, fecha, total):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.fecha = fecha
        self.total = total