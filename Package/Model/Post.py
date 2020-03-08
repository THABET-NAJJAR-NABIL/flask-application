from Package import app
from Package import db
from flask_marshmallow import Marshmallow
from datetime import datetime
ma = Marshmallow(app)


# Task Class/ Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id


# Task Schema
class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'date_posted', 'user_id')


# init Task schema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
