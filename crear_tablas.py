import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Conexión'))
from conexion import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN rol VARCHAR(20) DEFAULT 'usuario'")
    print("✅ Columna rol agregada")
except Exception as e:
    print(f"⚠️ Columna ya existe: {e}")

cursor.execute("UPDATE usuarios SET rol = 'admin' WHERE id_usuario = 1")
conn.commit()
conn.close()
print("✅ Usuario 1 establecido como admin")