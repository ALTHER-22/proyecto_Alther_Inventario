from flask import Flask, render_template, request, redirect
from inventario import db, Producto
import json
import csv

app = Flask(__name__)

# CONFIGURAR BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# CREAR BD
with app.app_context():
    db.create_all()

# ===============================
# RUTA PRINCIPAL
# ===============================
@app.route("/")
def index():
    productos = Producto.query.all()
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

    nuevo = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
    db.session.add(nuevo)
    db.session.commit()

    return redirect("/")

# ===============================
# ELIMINAR PRODUCTO
# ===============================
@app.route("/eliminar/<int:id>")
def eliminar(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect("/")

# ===============================
# EDITAR PRODUCTO
# ===============================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    producto = Producto.query.get(id)

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.precio = float(request.form["precio"])
        producto.cantidad = int(request.form["cantidad"])

        db.session.commit()
        return redirect("/")

    return render_template("editar.html", producto=producto)

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