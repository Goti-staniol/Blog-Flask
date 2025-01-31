from app import login_manager
from app.database.models import User

from flask import render_template
from flask import Blueprint

main_routes = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_routes.route('/')
def home():
    return render_template('index.html')


