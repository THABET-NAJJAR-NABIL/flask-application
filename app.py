import marshmallow as marshmallow
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:user@localhost:5432/db_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# init Marshmallow
ma = Marshmallow(app)


# Product Class/ Model
class Prodcut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def _init(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


# Product Schema

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


# init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# create a product
@app.route('/saveProduct', methods=['POST'], )
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    new_product = Prodcut(name, description, price, quantity)
    # db.session.add(new_product)
    # db.session.commit()
    print(new_product)
    return product_schema.jsonify(new_product)


# create a product
@app.route('/product', methods=['POST'], )
def get_product():
    data = request.get_data()
    print(data)

    name = request.args['name']

    return name, 200


# Run Server
@app.route("/", methods=['GET'])
def get():
    return jsonify({"msg": "Hello World!"})


if (__name__ == "__main__"):
    app.run(port=5000)
