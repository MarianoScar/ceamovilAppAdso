from flask import Flask, render_template

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')  

@app.route('/registro')
def registro():
    return render_template('registro-alumnos.html')

@app.route('/programar-clases-teoricas')
def programar_teoricas():
    return render_template('programar-clases-teoricas.html')

@app.route('/programar-clases-practicas')
def programar_practicas():
    return render_template('programar-clases-practicas.html')

@app.route('/ingreso-teoricas')
def teoricas():
    return render_template('teoricas.html')

@app.route('/ingreso-practicas')
def practicas():
    return render_template('practicas.html')

if __name__ == '__main__' :
    app.run(debug=True)