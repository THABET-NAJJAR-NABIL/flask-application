import marshmallow as marshmallow
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import psycopg2

# init app
app = Flask(__name__)
# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:user@localhost:5432/db_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# init Marshmallow
ma = Marshmallow(app)


# Product Class/ Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
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
    new_product = Product(name=name, description=description, price=price, quantity=quantity)
    db.session.add(new_product)
    db.session.commit()
    print(new_product)
    return product_schema.jsonify(new_product)


# update a  product
@app.route('/updateProduct/<id>', methods=['PUT'], )
def update_product(id):
    product = Product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity
    db.session.commit()
    return product_schema.jsonify(product)


# Delete a product by id
@app.route("/product/<id>", methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify(product_schema.dump(product))

# Get all products
@app.route("/products", methods=['GET'])
def get_all_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get a product by id
@app.route("/product/<id>", methods=['GET'])
def get_one_product(id):
    product = Product.query.get(id)
    return jsonify(product_schema.dump(product))


# create a product
@app.route('/product', methods=['POST'])
def get_product():
    data = request.json['name']
    return data, 200


# Run Server
@app.route("/", methods=['GET'])
def get():
    return jsonify({"msg": "Hello World!"})


if __name__ == "__main__":
    app.run(debug=False, port=5000)
