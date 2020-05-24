import marshmallow as marshmallow
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
import uuid
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import psycopg2

# init app
app = Flask(__name__)
# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:user@localhost:5432/db_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "my_secret_key_dont_use_it_smile"
db = SQLAlchemy(app)

# init Marshmallow
ma = Marshmallow(app)


# Task Class/ Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    text = db.Column(db.String(50))
    complete = db.Column(db.String(100))
    user_id = db.Column(db.String(100))

    def _init(self, text, complete, user_id):
        self.text = text
        self.complete = complete
        self.user_id = user_id


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


# User Class/ Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    public_id = db.Column(db.String(50), unique=True, )
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

    def _init(self, public_id, name, password, admin):
        self.public_id = public_id
        self.name = name
        self.password = password
        self.admin = admin


# Product Schema

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'name', 'admin')


# Task Schema
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text', 'complete', 'user_id')


# init Product schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# init Product schema
user_schema = ProductSchema()
users_schema = ProductSchema(many=True)

# init Task schema
Task_schema = ProductSchema()
Taskss_schema = ProductSchema(many=True)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token :
            return jsonify({'msg': 'Token is missing !!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'msg': 'Token is invalid !!'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'pass':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could Verify !', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@app.route('/unprotected')
def unprotected():
    return jsonify({'msg': 'Anyone can view this'})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'msg': 'this only available for people with valid token'})


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


@app.route("/user", methods=["POST"])
def create_user():
    public_id = str(uuid.uuid4())
    name = request.json['name']
    password = generate_password_hash(request.json['password'], method='sha256')
    admin = request.json['admin']
    new_user = User(public_id=public_id, name=name, password=password, admin=admin)
    print(new_user.password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "new user created"}), 200


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

# Only for test purpose /*upgrade*/


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


@app.route("/user", methods=["GET"])
def get_all_user():
    return ""


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    return ""


@app.route("/use/<user_id>", methods=["PUT"])
def update_user(user_id):
    return ""


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    return ""


if __name__ == "__main__":
    app.run(debug=False, port=5000)
