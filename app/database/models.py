from app import db
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(400), unique=True, nullable=False)
    password = db.Column(db.String)

    def get_id(self):
        return str(self.user_id)

class Post:
    ...

class Comment:
    ...
