import sqlite3


# --- 1. CLASE PRODUCTO ---
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Atributos encapsulados
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # Métodos Getters
    def get_id(self): return self.__id_producto

    def get_nombre(self): return self.__nombre

    def get_cantidad(self): return self.__cantidad

    def get_precio(self): return self.__precio

    # Métodos Setters
    def set_cantidad(self, nueva_cantidad): self.__cantidad = nueva_cantidad

    def set_precio(self, nuevo_precio): self.__precio = nuevo_precio

    # Uso de Colección (Diccionario) para estructurar la salida
    def to_dict(self):
        return {
            "id": self.__id_producto,
            "nombre": self.__nombre,
            "cantidad": self.__cantidad,
            "precio": self.__precio
        }


# --- 2. CLASE INVENTARIO (Gestión y Base de Datos) ---
class Inventario:
    def __init__(self, db_name="alther_tech.db"):
        self.db_name = db_name
        self.crear_tabla()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            # Crear tabla si no existe
            cursor.execute('''CREATE TABLE IF NOT EXISTS productos
                              (
                                  id
                                  TEXT
                                  PRIMARY
                                  KEY,
                                  nombre
                                  TEXT
                                  NOT
                                  NULL,
                                  cantidad
                                  INTEGER
                                  NOT
                                  NULL,
                                  precio
                                  REAL
                                  NOT
                                  NULL
                              )''')
            conn.commit()

    # Operación CRUD: CREATE (Añadir)
    def anadir_producto(self, producto):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                               (producto.get_id(), producto.get_nombre(), producto.get_cantidad(),
                                producto.get_precio()))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # El ID ya existe

    # Operación CRUD: READ (Mostrar todos usando Listas y Diccionarios)
    def obtener_todos(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            filas = cursor.fetchall()  # SQLite devuelve una lista de tuplas

            # Transformamos las tuplas en una lista de diccionarios para facilitar su uso
            lista_productos = []
            for fila in filas:
                prod = Producto(fila[0], fila[1], fila[2], fila[3])
                lista_productos.append(prod.to_dict())
            return lista_productos

    # Operación CRUD: UPDATE (Actualizar)
    def actualizar_producto(self, id_producto, nueva_cantidad, nuevo_precio):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
                           (nueva_cantidad, nuevo_precio, id_producto))
            conn.commit()

    # Operación CRUD: DELETE (Eliminar)
    def eliminar_producto(self, id_producto):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conn.commit()