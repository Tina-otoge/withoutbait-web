import flask
import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from app import db, login_manager
from app.db.models import User
from . import bp


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    class LoginForm(FlaskForm):
        username = StringField(validators=[DataRequired()])
        password = StringField(validators=[DataRequired()])

    form = LoginForm()

    if not form.validate_on_submit():
        return flask.render_template('login.html', form=form)

    user = db.session.query(User).filter_by(username=form.username.data).first()
    if not user:
        raise Exception(f'User {user} not found')
    if not user.check_password(form.password.data):
        raise Exception('Invalid password')
    flask_login.login_user(user, remember=True)

    return flask.redirect('/')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    class RegisterForm(FlaskForm):
        username = StringField(validators=[DataRequired()])
        password = StringField(validators=[DataRequired()])

    form = RegisterForm()

    if not form.validate_on_submit():
        return flask.render_template('register.html', form=form)

    user = db.session.query(User).filter_by(username=form.username.data).first()
    if user:
        raise Exception(f'User {user} already exists')
    user = User(username=form.username.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flask_login.login_user(user, remember=True)

    return flask.redirect('/')


@bp.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect('/')
