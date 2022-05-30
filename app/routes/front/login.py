import flask
import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from app import login_manager, db
from app.db.models import User
from . import bp


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    class LoginForm(FlaskForm):
        username = StringField(validators=[DataRequired()])
        password = PasswordField(validators=[DataRequired()])

    def render():
        return flask.render_template('login.html', form=form)

    form = LoginForm()

    if not form.validate_on_submit():
        return render()

    user = db.session.query(User).filter_by(username=form.username.data).first()
    if not user:
        flask.flash(f'User "{form.username.data}" not found')
        return render()

    if not user.check_password(form.password.data):
        flask.flash('Wrong password')
        return render()

    flask_login.login_user(user, remember=True)

    return flask.redirect('/')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    class RegisterForm(FlaskForm):
        username = StringField(validators=[DataRequired()])
        password = PasswordField(validators=[DataRequired()])

    form = RegisterForm()

    if not form.validate_on_submit():
        return flask.render_template('register.html', form=form)

    user = db.session.query(User).filter_by(username=form.username.data).first()
    if user:
        flask.flash('Username already taken')
        return flask.render_template('register.html', form=form)
    user = User(username=form.username.data, password=form.password.data)
    db.add(user, save=True)
    flask_login.login_user(user, remember=True)

    return flask.redirect('/')


@bp.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect('/')
