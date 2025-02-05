import os
import uuid

from flask import (
    render_template,
    Blueprint,
    flash,
    url_for,
    redirect,
    current_app,
    send_from_directory
)

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

from app import login_manager, db
from app.database.models import User, Post
from app.forms import (
    RegistrationForm,
    LoginForm,
    PostForm,
    SearchForm,
    validate_email,
    validate_username
)

from fuzzywuzzy import process


main_route = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main_route.route('/', methods=['POST', 'GET'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        post_tags = db.session.query(Post.tags).all()
        post_tags = [tag[0] for tag in post_tags]
        matches = process.extract(form.text.data, post_tags, limit=1)
        tags = [match[0] for match in matches]
        posts = Post.query.filter(Post.tags.like(f"%{tags[0]}%")).all()

        return render_template('index.html', posts=posts, form=form)

    posts = Post.query.all()
    return render_template('index.html', posts=posts, form=form)


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
    form = PostForm()
    if form.validate_on_submit():
        photo_name = None
        if form.photo.data:
            photo = form.photo.data
            photo_name = (str(uuid.uuid4()) + '.png').replace('-', '')
            photo_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                photo_name
            )
            photo.save(photo_path)
        post = Post(
            user_id=current_user.user_id,
            title=form.title.data,
            description=form.description.data,
            tags=form.tags.data,
            photo_name=photo_name if photo_name else ''
        )
        db.session.add(post)
        db.session.commit()
        db.session.close()

        return redirect(url_for('main.home'))
    return render_template('post.html', form=form)


@main_route.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)