from flask import Flask, render_template

app = Flask(__name__)

# 1. RUTA PRINCIPAL (Ahora usa index.html)
@app.route('/')
def index():
    return render_template('index.html')

# 2. RUTA ACERCA DE (Nueva para esta semana)
@app.route('/about')
def about():
    return render_template('about.html')

# 3. RUTA DINÁMICA (Usa item.html y pasa el código)
@app.route('/item/<codigo>')
def consultar_item(codigo):
    return render_template('item.html', codigo=codigo)

if __name__ == '__main__':
    app.run(debug=True)