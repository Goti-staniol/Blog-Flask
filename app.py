from cfg import SECRET_KEY

from db.models import Base, engine
from db.methods import check_user, add_new_user, get_user, get_user_by_email

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager(app)
login_manager.login_view = 'login'

registered_users = {}
has_posts = True
Base.metadata.create_all(engine)

@login_manager.user_loader
def load_user(user_id):
    user = get_user(user_id)
    return user.user_id

@app.route('/', methods=['GET', 'POST'])
def main_handler():
    if has_posts:
        return render_template('available_posts_main.html')

    return render_template('no_posts_main.html')

@app.route('/register', methods=['GET', 'POST'])
def registration_handler():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))

        add_new_user(
            username,
            email,
            password
        )

        flash('Успешная регестрация!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = get_user_by_email(email)

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Вы успешно вошли!', 'success')

            return redirect(url_for('main_handler'))

        flash('Неправильный email или пароль!', 'danger')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
