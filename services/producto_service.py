import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Conexión'))
from conexion import get_connection

def get_all_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def get_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    conn.close()
    return producto

def create_producto(nombre, precio, cantidad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (%s, %s, %s)",
                   (nombre, precio, cantidad))
    conn.commit()
    conn.close()

def update_producto(id, nombre, precio, cantidad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET nombre=%s, precio=%s, cantidad=%s WHERE id=%s",
                   (nombre, precio, cantidad, id))
    conn.commit()
    conn.close()

def delete_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    conn.close()

def get_all_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def get_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def create_cliente(nombre, email, telefono, direccion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s)",
                   (nombre, email, telefono, direccion))
    conn.commit()
    conn.close()

def update_cliente(id, nombre, email, telefono, direccion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET nombre=%s, email=%s, telefono=%s, direccion=%s WHERE id_cliente=%s",
                   (nombre, email, telefono, direccion, id))
    conn.commit()
    conn.close()

def delete_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id,))
    conn.commit()
    conn.close()