"""
DOCUMENTACIÓN DEL SISTEMA DE GESTIÓN DE INVENTARIO
--------------------------------------------------
1. Estructura de Datos (Colecciones):
   - Se utiliza un Diccionario (self.productos = {}) como estructura principal en memoria.
   - La clave (Key) del diccionario es el ID del producto.
   - El valor (Value) es el objeto de la clase Producto.
   - JUSTIFICACIÓN: El uso de un diccionario permite búsquedas, inserciones y eliminaciones
     extremadamente rápidas (complejidad O(1)) accediendo directamente por ID, lo cual es
     mucho más eficiente que recorrer una lista (O(n)) cada vez que se necesita un producto.

2. Persistencia de Datos (SQLite):
   - Se utiliza la librería sqlite3 para crear una base de datos local 'inventario.db'.
   - Al iniciar el programa, los datos se leen de la BD y se cargan en el diccionario (Caché).
   - Cada vez que se agrega, elimina o modifica un producto, se actualiza tanto el
     diccionario (para uso inmediato) como la base de datos (para almacenamiento permanente).

3. POO:
   - Clase Producto: Define la estructura de los datos.
   - Clase Inventario: Encapsula la lógica de negocio y manejo de datos.
"""
import sqlite3


# -----------------------------------------------------------------------------
# CLASE PRODUCTO (POO)
# -----------------------------------------------------------------------------
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Métodos Getters y Setters
    def get_id(self):
        return self.id

    def get_nombre(self):
        return self.nombre

    def set_cantidad(self, nueva_cantidad):
        self.cantidad = nueva_cantidad

    def set_precio(self, nuevo_precio):
        self.precio = nuevo_precio

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Cant: {self.cantidad} | Precio: ${self.precio:.2f}"


# -----------------------------------------------------------------------------
# CLASE INVENTARIO (POO + Colecciones + SQLite)
# -----------------------------------------------------------------------------
class Inventario:
    def __init__(self, db_name='inventario.db'):
        self.db_name = db_name
        # Colección principal: Diccionario {id: ObjetoProducto}
        # Usamos un diccionario para cumplir el requisito de "Colecciones" y búsqueda rápida
        self.productos = {}
        self.conexion_db()
        self.cargar_inventario_desde_db()

    def conexion_db(self):
        """Crea la tabla 'productos' en SQLite si no existe."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS productos
                               (
                                   id
                                   INTEGER
                                   PRIMARY
                                   KEY
                                   UNIQUE,
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
                               )
                               ''')
                conn.commit()
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")

    def cargar_inventario_desde_db(self):
        """Lee todos los datos de SQLite y los carga en el diccionario self.productos."""
        self.productos = {}  # Limpiamos el diccionario para recargar
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM productos")
                filas = cursor.fetchall()
                for fila in filas:
                    # fila tiene la forma: (id, nombre, cantidad, precio)
                    nuevo_prod = Producto(fila[0], fila[1], fila[2], fila[3])
                    # Guardamos en el diccionario usando el ID como clave
                    self.productos[fila[0]] = nuevo_prod
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def agregar_producto(self, producto):
        """Añade un producto a la BD y actualiza el diccionario."""
        if producto.id in self.productos:
            print("Error: Ya existe un producto con ese ID.")
            return

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                               (producto.id, producto.nombre, producto.cantidad, producto.precio))
                conn.commit()

            # Si guardó bien en BD, actualizamos la colección en memoria
            self.productos[producto.id] = producto
            print("Producto agregado exitosamente.")
        except sqlite3.IntegrityError:
            print("Error: El ID ya existe en la base de datos.")
        except Exception as e:
            print(f"Error al guardar: {e}")

    def eliminar_producto(self, id_producto):
        """Elimina el producto de la BD y del diccionario."""
        if id_producto in self.productos:
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                    conn.commit()

                # Eliminamos del diccionario local
                del self.productos[id_producto]
                print("Producto eliminado.")
            except Exception as e:
                print(f"Error al eliminar de BD: {e}")
        else:
            print("Error: Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cant=None, nuevo_precio=None):
        """Actualiza cantidad o precio."""
        if id_producto in self.productos:
            prod = self.productos[id_producto]

            # Actualizamos el objeto en memoria
            if nueva_cant is not None:
                prod.set_cantidad(nueva_cant)
            if nuevo_precio is not None:
                prod.set_precio(nuevo_precio)

            # Actualizamos en la base de datos
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    if nueva_cant is not None:
                        cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cant, id_producto))
                    if nuevo_precio is not None:
                        cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, id_producto))
                    conn.commit()
                print("Producto actualizado correctamente.")
            except Exception as e:
                print(f"Error al actualizar BD: {e}")
        else:
            print("Error: Producto no encontrado.")

    def buscar_producto(self, nombre):
        """Busca productos por nombre (no case-sensitive)."""
        encontrados = False
        print("\n--- Resultados de búsqueda ---")
        for prod in self.productos.values():
            if nombre.lower() in prod.nombre.lower():
                print(prod)
                encontrados = True
        if not encontrados:
            print("No se encontraron productos coincidente.")

    def listar_productos(self):
        """Muestra todo el inventario."""
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\n--- Listado Completo del Inventario ---")
            for prod in self.productos.values():
                print(prod)


# -----------------------------------------------------------------------------
# MENÚ INTERACTIVO DE CONSOLA
# -----------------------------------------------------------------------------
def menu():
    tienda = Inventario()

    while True:
        print("\n" + "=" * 40)
        print(" SISTEMA DE GESTIÓN DE INVENTARIO")
        print("=" * 40)
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad o precio")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            try:
                id_prod = int(input("Ingrese ID único (numérico): "))
                nombre = input("Ingrese nombre del producto: ")
                cant = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                nuevo_prod = Producto(id_prod, nombre, cant, precio)
                tienda.agregar_producto(nuevo_prod)
            except ValueError:
                print("Error: Asegúrese de ingresar números válidos para ID, cantidad y precio.")

        elif opcion == '2':
            try:
                id_prod = int(input("Ingrese el ID del producto a eliminar: "))
                tienda.eliminar_producto(id_prod)
            except ValueError:
                print("Error: El ID debe ser un número.")

        elif opcion == '3':
            try:
                id_prod = int(input("Ingrese el ID del producto a actualizar: "))
                print("(Deje vacío y presione Enter si no desea cambiar el valor)")
                n_cant = input("Nueva cantidad: ")
                n_precio = input("Nuevo precio: ")

                cant_val = int(n_cant) if n_cant else None
                precio_val = float(n_precio) if n_precio else None

                tienda.actualizar_producto(id_prod, cant_val, precio_val)
            except ValueError:
                print("Error: Ingrese valores numéricos válidos.")

        elif opcion == '4':
            nombre = input("Ingrese el nombre a buscar: ")
            tienda.buscar_producto(nombre)

        elif opcion == '5':
            tienda.listar_productos()

        elif opcion == '6':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, intente de nuevo.")


# Este bloque asegura que el menú solo corra si ejecutamos este archivo directamente
if __name__ == "__main__":
    menu()