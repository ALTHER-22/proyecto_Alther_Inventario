import pymysql

def get_connection():
    conexion = pymysql.connect(
        host="sql10.freesqldatabase.com",
        user="sql10820958",
        password="cnKVd4qadi",
        database="sql10820958",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conexion