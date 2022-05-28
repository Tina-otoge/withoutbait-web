import flask
import flask_login
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

from app import db
from app.db.models import User
from . import bp


def admin_check():
    if not flask_login.current_user.is_admin:
        return flask.redirect('/')


@bp.route('/admin')
def tools():
    admin_check()
    return flask.render_template('admin/tools_list.html')


class UseraddForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    admin = BooleanField(default=True)


@bp.route('/admin/useradd', methods=['GET', 'POST'])
def useradd():
    admin_check()

    form = UseraddForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.name.data).first()
        if not user:
            flask.flash('User not found')
        else:
            user.is_admin = form.admin.data
            flask.flash(f'{user} admin state set to {user.is_admin}')
            db.session.commit()

    admins = db.session.query(User).filter_by(is_admin=True)

    return flask.render_template('admin/add_admin.html', form=form, admins=admins)
