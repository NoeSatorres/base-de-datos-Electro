from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/electrodomesticos'
db = SQLAlchemy(app)

class Electro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    modelo = db.Column(db.String(30), unique=True, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)  

    def __init__(self, nombre, modelo, cantidad, precio):
        self.nombre = nombre
        self.modelo = modelo
        self.cantidad = cantidad  
        self.precio = precio


# Agregar un producto
@app.route('/electrodomesticos', methods=['POST'])
def agregar_electrodomestico():
    data = request.get_json()
    nuevo_electrodomestico = Electro(
        nombre=data['nombre'],
        modelo=data['modelo'],
        cantidad=data['cantidad'],
        precio=data['precio']
    )
    db.session.add(nuevo_electrodomestico)
    db.session.commit()
    return jsonify({'message': 'Se agregó un nuevo electrodomestico'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
