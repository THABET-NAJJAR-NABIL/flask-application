# Product Class/ Model
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# init app
app = Flask(__name__)
# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:user@localhost:5432/db_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
