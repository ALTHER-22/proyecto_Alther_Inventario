import pymysql
import os

def get_connection():
    conexion = pymysql.connect(
        host=os.environ.get('DB_HOST', 'hopper.proxy.rlwy.net'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'EFNfQBBMPdmkRApMmsRxTquCSftFnJjd'),
        database=os.environ.get('DB_NAME', 'railway'),
        port=int(os.environ.get('DB_PORT', '55085')),
        cursorclass=pymysql.cursors.DictCursor
    )
    return conexion