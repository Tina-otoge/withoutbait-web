import flask
from flask_wtf import FlaskForm
from wtforms.fields import StringField, BooleanField
from wtforms.validators import DataRequired


from app import db
from app.db.models import User
from . import bp


class UseraddForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    admin = BooleanField(default=True)


@bp.route('/useradd', methods=['GET', 'POST'])
def useradd():
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

