from Package import app, db
from datetime import datetime
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


# Product Class/ Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    date_add = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, description, price, quantity, user_id):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.user_id = user_id


# Task Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description', 'price', 'quantity', 'date_add', 'user_id')


# init Task schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
