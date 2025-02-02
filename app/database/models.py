from app import db
from flask_login import UserMixin
from datetime import datetime, UTC


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(400), unique=True, nullable=False)
    password = db.Column(db.String)

    def get_id(self):
        return str(self.user_id)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    photo_path = db.Column(db.String, nullable=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    tags = db.Column(db.String(80), nullable=True)
    # created_at = db.Column(db.DateTime, default=datetime.now(UTC))


class Comment:
    ...
