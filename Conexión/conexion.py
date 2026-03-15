import pymysql

def get_connection():
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="proyecto_alther_inventario",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conexion