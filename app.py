from flask import Flask, render_template, request, redirect
from inventario import Inventario

app = Flask(__name__)
inventario = Inventario()


@app.route("/")
def inicio():
    productos = inventario.obtener_productos()
    return render_template("index.html", productos=productos)


@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    cantidad = request.form["cantidad"]

    inventario.agregar_producto(nombre, precio, cantidad)
    return redirect("/")


@app.route("/eliminar/<int:id>")
def eliminar(id):
    inventario.eliminar_producto(id)
    return redirect("/")


@app.route("/buscar", methods=["POST"])
def buscar():
    texto = request.form["buscar"]
    productos = inventario.buscar_producto(texto)
    return render_template("index.html", productos=productos)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)