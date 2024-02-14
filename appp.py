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

# LISTAR


@app.route('/electrodomesticos', methods=['GET'])
def obtener_electrodomestico():
    electrodomesticos = Electro.query.all()
    electrodomesticos_json = [{'nombre': electrodomestico.nombre, 'modelo': electrodomestico.modelo,
                              'cantidad': electrodomestico.cantidad, 'precio': electrodomestico.precio} for electrodomestico in electrodomesticos]
    return jsonify(electrodomesticos_json),200

#BUSCAR
@app.route('/electrodomesticos/buscar', methods=['POST'])
def buscar_electrodomestico():
    data = request.get_json()
    modelo = data.get('modelo')
    if modelo:
        electrodomestico = Electro.query.filter_by(modelo=modelo).first()
        if electrodomestico:
            electrodomesticos_json = [{'nombre': electrodomestico.nombre, 'modelo': electrodomestico.modelo,
                              'cantidad': electrodomestico.cantidad, 'precio': electrodomestico.precio}]
            return jsonify (electrodomesticos_json), 200
        return jsonify ({'message': 'Electrodomestico no encontrado'}),404
            


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
