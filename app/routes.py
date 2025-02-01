from flask import render_template, Blueprint, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from app import login_manager, db
from app.forms import RegistrationForm, LoginForm
from app.database.models import User


main_route = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main_route.route('/')
def home():
    return render_template('index.html')


@main_route.route('/registration', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    try:
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            db.session.close()

            flash(
                'Регестрация прошла успешно! Пожалйуста войдите с этими данными!',
                'success'
            )
            return redirect(url_for('main.login'))
    except IntegrityError:
        db.session.rollback()
        flash("Ошибка: имя пользователя или email уже заняты.", "danger")
    finally:
        db.session.close()

    return render_template(
        'registration.html',
        title='Регистрация',
        form=form
    )


@main_route.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash(
                'Вход не удался! Проверьте данные и войдите еще раз!',
                'danger'
            )
    return render_template(
        'login.html',
        title='Вход',
        form=form
    )


@main_route.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    return 'Hello'






