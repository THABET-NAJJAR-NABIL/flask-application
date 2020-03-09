from flask import request, jsonify, make_response
import uuid
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from Package import app, db, bcrypt
from Package.Model.Product import Product, products_schema, product_schema
from Package.Model.User import User, users_schema, user_schema
from Package.Model.Post import Post, post_schema, posts_schema
from flask_cors import CORS, cross_origin
from flask_login import login_user, current_user, logout_user
cors = CORS(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'msg': 'Token is missing !!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'msg': 'Token is invalid !!'}), 403
        return f(*args, **kwargs)

    return decorated


""" USER ROUTES"""


@app.route("/register", methods=["POST"])
def register():
    hashed_password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    username = request.json['username']
    email = request.json['email']
    admin = request.json['admin']
    new_user = User(username=username, email=email, password=hashed_password, admin=admin)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 200


@app.route("/useUpdate/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    user.email = request.json['email']
    user.admin = request.json['admin']
    db.session.commit()
    return user_schema.jsonify(user), 200


@app.route("/users", methods=["GET"])
def get_all_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route("/verifyUsername", methods=["POST"])
def verify_username():
    user = User.query.filter_by(username=request.json['username']).first()
    if user:
        return jsonify({'msg': 'username already exist, choose another one please !!'}), 403
    else:
        return jsonify({'msg': 'you can use this username!!'}), 200


@app.route("/verifyEmail", methods=["POST"])
def verify_email():
    user = User.query.filter_by(email=request.json['email']).first()
    if user:
        return jsonify({'msg': 'email already exist, choose another one please !!'}), 403
    else:
        return jsonify({'msg': 'you can use this email!!'}), 200


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user_schema.dump(user))


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(product_schema.dump(user))


@app.route('/login', methods=["POST"])
def login():
    if not current_user.is_authenticated:
        user = User.query.filter_by(email=request.json['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            login_user(user)
            token = jwt.encode({'user': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                           app.config['SECRET_KEY'])
            return jsonify({'msg': 'Connected', 'token': token.decode('UTF-8')}), 200
        else:
            return jsonify({'msg': 'Bad credentials'}), 401
    else:
        print('CURRENT USER ID', current_user.admin)
        return jsonify({'msg': 'Already connected'}), 200


@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'msg': 'Session deleted'}), 200


@app.route('/isLoggedIn', methods=['GET'])
def is_logged_in():
    return jsonify({'is_connected': current_user.is_authenticated}), 200


@app.route('/about', methods=['POST'])
@cross_origin()
def about():
    username = request.json['username']
    password = request.json['password']
    return jsonify({'username': username, 'password': password})


@app.route('/')
@app.route('/home')
def home():
    return jsonify({'msg': 'Home page !!'})


""" PRODUCT ROUTES"""


# create a product
@app.route('/saveProduct', methods=['POST'], )
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    user_id = request.json['user_id']
    new_product = Product(name=name, description=description, price=price, quantity=quantity, user_id= user_id)
    db.session.add(new_product)
    db.session.commit()
    print(new_product)
    return product_schema.jsonify(new_product)


# update a  product
@app.route('/updateProduct/<product_id>', methods=['PUT'], )
def update_product(product_id):
    product = Product.query.get(product_id)
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    product.description = description
    product.price = price
    product.quantity = quantity
    db.session.commit()
    return product_schema.jsonify(product)


# Delete a product by id
@app.route("/product/<product_id>", methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
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
@app.route("/product/<product_id>", methods=['GET'])
def get_one_product(product_id):
    product = Product.query.get(product_id)
    return jsonify(product_schema.dump(product))


# create a post
@app.route('/savePost', methods=['POST'], )
def add_post():
    title = request.json['title']
    content = request.json['content']
    user_id = request.json['user_id']
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    print(new_post)
    return post_schema.jsonify(new_post)


# update a  post
@app.route('/updatePpost/<post_id>', methods=['PUT'], )
def update_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.json['title']
    post.content = request.json['content']
    db.session.commit()
    return product_schema.jsonify(post)


# Delete a post by id
@app.route("/product/<post_id>", methods=['DELETE'])
def delete_post(post_id):
    post = Product.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify(product_schema.dump(post))


# Get all posts
@app.route("/products", methods=['GET'])
def get_all_posts():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result)


# Get a post by id
@app.route("/product/<post_id>", methods=['GET'])
def get_one_post(post_id):
    post = Post.query.get(post_id)
    return jsonify(post_schema.dump(post))

