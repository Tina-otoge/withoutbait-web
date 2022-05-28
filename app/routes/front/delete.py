from flask_wtf import FlaskForm
from wtforms.fields import SubmitField

class DeleteForm(FlaskForm):
    submit = SubmitField()
