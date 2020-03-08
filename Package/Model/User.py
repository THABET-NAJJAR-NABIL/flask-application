from Package import app
from Package import db
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


# User Class/ Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    admin = db.Column(db.Boolean)

    def __init__(self, username, email, password, admin):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin


# Task Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'Posts', 'admin')


# init Task schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
