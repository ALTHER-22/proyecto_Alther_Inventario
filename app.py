from flask import Flask, render_template, request, redirect, flash, make_response
import json
import csv
import sys
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.producto import Producto, Cliente, Pedido
from services.producto_service import (get_all_productos, get_producto, create_producto,
                                        update_producto, delete_producto, get_all_clientes,
                                        get_cliente, create_cliente, update_cliente, delete_cliente)
from fpdf import FPDF

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
        from models.usuario import Usuario
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
            from models.usuario import Usuario
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
# INICIO
# ===============================
@app.route("/")
@login_required
def index():
    productos = get_all_productos()
    return render_template("index.html", productos=productos)

# ===============================
# AGREGAR PRODUCTO DESDE INICIO
# ===============================
@app.route("/agregar", methods=["POST"])
@login_required
def agregar():
    create_producto(request.form["nombre"],
                    float(request.form["precio"]),
                    int(request.form["cantidad"]))
    return redirect("/")

# ===============================
# ACERCA DE
# ===============================
@app.route("/about")
@login_required
def about():
    return render_template("about.html")

# ===============================
# PRODUCTOS - CRUD
# ===============================
@app.route("/productos")
@login_required
def lista_productos():
    productos = get_all_productos()
    return render_template("productos/lista.html", productos=productos)

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    if request.method == "POST":
        create_producto(request.form["nombre"],
                        float(request.form["precio"]),
                        int(request.form["cantidad"]))
        return redirect("/productos")
    return render_template("productos/form.html", titulo="Nuevo Producto", producto=None)

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    producto = get_producto(id)
    if request.method == "POST":
        update_producto(id, request.form["nombre"],
                        float(request.form["precio"]),
                        int(request.form["cantidad"]))
        return redirect("/productos")
    return render_template("productos/form.html", titulo="Editar Producto", producto=producto)

@app.route("/productos/eliminar/<int:id>")
@login_required
def eliminar_producto(id):
    delete_producto(id)
    return redirect("/productos")

# ===============================
# REPORTE PDF
# ===============================
@app.route("/productos/reporte_pdf")
@login_required
def reporte_pdf():
    productos = get_all_productos()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Reporte de Productos", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(20, 10, "ID", border=1)
    pdf.cell(80, 10, "Nombre", border=1)
    pdf.cell(40, 10, "Precio", border=1)
    pdf.cell(40, 10, "Cantidad", border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    for p in productos:
        pdf.cell(20, 10, str(p['id']), border=1)
        pdf.cell(80, 10, str(p['nombre']), border=1)
        pdf.cell(40, 10, f"${p['precio']}", border=1)
        pdf.cell(40, 10, str(p['cantidad']), border=1, new_x="LMARGIN", new_y="NEXT")
    pdf_bytes = bytes(pdf.output())
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_productos.pdf'
    return response

# ===============================
# CLIENTES - CRUD
# ===============================
@app.route("/clientes")
@login_required
def lista_clientes():
    clientes = get_all_clientes()
    return render_template("clientes/lista.html", clientes=clientes)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    if request.method == "POST":
        create_cliente(request.form["nombre"], request.form["email"],
                       request.form["telefono"], request.form["direccion"])
        return redirect("/clientes")
    return render_template("clientes/form.html", titulo="Nuevo Cliente", cliente=None)

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):
    cliente = get_cliente(id)
    if request.method == "POST":
        update_cliente(id, request.form["nombre"], request.form["email"],
                       request.form["telefono"], request.form["direccion"])
        return redirect("/clientes")
    return render_template("clientes/form.html", titulo="Editar Cliente", cliente=cliente)

@app.route("/clientes/eliminar/<int:id>")
@login_required
def eliminar_cliente(id):
    delete_cliente(id)
    return redirect("/clientes")

# ===============================
# USUARIOS - CRUD
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
# GUARDAR TXT / JSON / CSV
# ===============================
@app.route("/guardar_txt", methods=["POST"])
@login_required
def guardar_txt():
    nombre = request.form["nombre"]
    with open("inventario/data/datos.txt", "a") as f:
        f.write(nombre + "\n")
    return redirect("/datos")

@app.route("/guardar_json", methods=["POST"])
@login_required
def guardar_json():
    nombre = request.form["nombre"]
    data = {"nombre": nombre}
    with open("inventario/data/datos.json", "w") as f:
        json.dump(data, f)
    return redirect("/datos")

@app.route("/guardar_csv", methods=["POST"])
@login_required
def guardar_csv():
    nombre = request.form["nombre"]
    with open("inventario/data/datos.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([nombre])
    return redirect("/datos")

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