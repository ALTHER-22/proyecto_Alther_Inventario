from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import json
import csv
import sys
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Conexión'))
from conexion import get_connection

app = Flask(__name__)
app.secret_key = 'clave_secreta_inventario_2024'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesión para acceder.'

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    u = cursor.fetchone()
    conn.close()
    if u:
        return Usuario(u['id_usuario'], u['nombre'], u['email'], u['password'])
    return None

# ===============================
# LOGIN
# ===============================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        u = cursor.fetchone()
        conn.close()

        if u and check_password_hash(u['password'], password):
            usuario = Usuario(u['id_usuario'], u['nombre'], u['email'], u['password'])
            login_user(usuario)
            return redirect("/")
        else:
            flash("Email o contraseña incorrectos.")

    return render_template("login.html")

# ===============================
# REGISTRO
# ===============================
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                       (nombre, email, password))
        conn.commit()
        conn.close()
        flash("Usuario registrado correctamente. Inicia sesión.")
        return redirect("/login")

    return render_template("registro.html")

# ===============================
# LOGOUT
# ===============================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# ===============================
# RUTA PRINCIPAL (protegida)
# ===============================
@app.route("/")
@login_required
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
@login_required
def about():
    return render_template("about.html")

# ===============================
# AGREGAR PRODUCTO
# ===============================
@app.route("/agregar", methods=["POST"])
@login_required
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
@login_required
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
@login_required
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
# VER USUARIOS (protegida)
# ===============================
@app.route("/usuarios")
@login_required
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
@login_required
def agregar_usuario():
    nombre = request.form["nombre"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                   (nombre, email, password))
    conn.commit()
    conn.close()
    return redirect("/usuarios")

# ===============================
# ELIMINAR USUARIO
# ===============================
@app.route("/eliminar_usuario/<int:id>")
@login_required
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
@login_required
def editar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        cursor.execute("UPDATE usuarios SET nombre=%s, email=%s, password=%s WHERE id_usuario=%s",
                       (nombre, email, password, id))
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
@login_required
def guardar_txt():
    nombre = request.form["nombre"]
    with open("inventario/data/datos.txt", "a") as f:
        f.write(nombre + "\n")
    return redirect("/datos")

# ===============================
# GUARDAR JSON
# ===============================
@app.route("/guardar_json", methods=["POST"])
@login_required
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
@login_required
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
@login_required
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