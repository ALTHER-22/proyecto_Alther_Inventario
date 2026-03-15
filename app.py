from flask import Flask, render_template, request, redirect
import pymysql
import json
import csv
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Conexión'))
from conexion import get_connection

app = Flask(__name__)

# ===============================
# RUTA PRINCIPAL
# ===============================
@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("index.html", productos=productos)

# ===============================
# PAGINA ACERCA DE
# ===============================
@app.route("/about")
def about():
    return render_template("about.html")

# ===============================
# AGREGAR PRODUCTO
# ===============================
@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    precio = float(request.form["precio"])
    cantidad = int(request.form["cantidad"])

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (%s, %s, %s)",
                   (nombre, precio, cantidad))
    conn.commit()
    conn.close()
    return redirect("/")

# ===============================
# ELIMINAR PRODUCTO
# ===============================
@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# ===============================
# EDITAR PRODUCTO
# ===============================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        cantidad = int(request.form["cantidad"])
        cursor.execute("UPDATE productos SET nombre=%s, precio=%s, cantidad=%s WHERE id=%s",
                       (nombre, precio, cantidad, id))
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template("editar.html", producto=producto)

# ===============================
# VER USUARIOS
# ===============================
@app.route("/usuarios")
def usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    lista_usuarios = cursor.fetchall()
    conn.close()
    return render_template("usuarios.html", usuarios=lista_usuarios)

# ===============================
# AGREGAR USUARIO
# ===============================
@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():
    nombre = request.form["nombre"]
    mail = request.form["mail"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
                   (nombre, mail, password))
    conn.commit()
    conn.close()
    return redirect("/usuarios")

# ===============================
# ELIMINAR USUARIO
# ===============================
@app.route("/eliminar_usuario/<int:id>")
def eliminar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
    conn.commit()
    conn.close()
    return redirect("/usuarios")

# ===============================
# EDITAR USUARIO
# ===============================
@app.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        mail = request.form["mail"]
        password = request.form["password"]
        cursor.execute("UPDATE usuarios SET nombre=%s, mail=%s, password=%s WHERE id_usuario=%s",
                       (nombre, mail, password, id))
        conn.commit()
        conn.close()
        return redirect("/usuarios")

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id,))
    usuario = cursor.fetchone()
    conn.close()
    return render_template("editar_usuario.html", usuario=usuario)

# ===============================
# GUARDAR TXT
# ===============================
@app.route("/guardar_txt", methods=["POST"])
def guardar_txt():
    nombre = request.form["nombre"]
    with open("inventario/data/datos.txt", "a") as f:
        f.write(nombre + "\n")
    return redirect("/datos")

# ===============================
# GUARDAR JSON
# ===============================
@app.route("/guardar_json", methods=["POST"])
def guardar_json():
    nombre = request.form["nombre"]
    data = {"nombre": nombre}
    with open("inventario/data/datos.json", "w") as f:
        json.dump(data, f)
    return redirect("/datos")

# ===============================
# GUARDAR CSV
# ===============================
@app.route("/guardar_csv", methods=["POST"])
def guardar_csv():
    nombre = request.form["nombre"]
    with open("inventario/data/datos.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([nombre])
    return redirect("/datos")

# ===============================
# VER DATOS GUARDADOS
# ===============================
@app.route("/datos")
def ver_datos():
    try:
        with open("inventario/data/datos.txt") as f:
            txt = f.readlines()
    except:
        txt = []

    try:
        with open("inventario/data/datos.json") as f:
            json_data = json.load(f)
    except:
        json_data = {}

    csv_data = []
    try:
        with open("inventario/data/datos.csv") as f:
            reader = csv.reader(f)
            csv_data = list(reader)
    except:
        pass

    return render_template("datos.html", txt=txt, json_data=json_data, csv_data=csv_data)

if __name__ == "__main__":
    app.run(debug=True)