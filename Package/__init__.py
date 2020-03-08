from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# init app
app = Flask(__name__)
# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/db_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "my_secret_key_dont_use_it_smile"
db = SQLAlchemy(app)

# init Marshmallow
bcrypt = Bcrypt(app)

from Package import routes
