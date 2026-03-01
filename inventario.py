import sqlite3


class Inventario:

    def __init__(self, db_name="inventario.db"):
        self.db_name = db_name
        self.crear_tabla()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL
            )
        """)
        con.commit()
        con.close()

    def agregar_producto(self, nombre, precio, cantidad):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)",
            (nombre, precio, cantidad)
        )
        con.commit()
        con.close()

    def obtener_productos(self):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        con.close()
        return productos

    def eliminar_producto(self, id):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        con.commit()
        con.close()

    def buscar_producto(self, texto):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute(
            "SELECT * FROM productos WHERE nombre LIKE ?",
            ('%' + texto + '%',)
        )
        productos = cursor.fetchall()
        con.close()
        return productos