from flask import Flask

app = Flask(__name__)

# 1. RUTA PRINCIPAL
@app.route('/')
def index():
    return """
    <h1>Bienvenido al Sistema de Inventario - Alther Tech</h1>
    <p><b>Propósito:</b> Control de stock automatizado y gestión de suministros en tiempo real.</p>
    <hr>
    <p>Para probar una consulta, escriba en la barra de direcciones: <b>/item/TU_CODIGO</b></p>
    """

# 2. RUTA DINÁMICA
@app.route('/item/<codigo>')
def consultar_item(codigo):
    return f"""
    <h2>Detalles del Inventario</h2>
    <p>Producto consultado con Código: <b>{codigo}</b></p>
    <p>Estado actual: <b>Disponible en bodega principal.</b></p>
    """

if __name__ == '__main__':
    app.run(debug=True)