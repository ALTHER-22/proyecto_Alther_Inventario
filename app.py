from flask import Flask

app = Flask(__name__)

# Paso 2 de la tarea: Ruta principal con nombre y propósito del negocio
@app.route('/')
def index():
    return """
    <h1>Bienvenido al Sistema de Inventario - Alther Tech</h1>
    <p>Propósito: Control automatizado de stock y gestión de suministros en tiempo real.</p>
    <hr>
    <p>Use la ruta /item/codigo para consultar un producto.</p>
    """

# Paso 3 de la tarea: Ruta dinámica adaptada a Inventario (/item/<codigo>)
@app.route('/item/<codigo>')
def consultar_item(codigo):
    return f"<h2>Consulta de Inventario</h2><p>Producto con Código: <b>{codigo}</b> – Consulta exitosa: Disponible en bodega.</p>"

if __name__ == '__main__':
    app.run(debug=True)