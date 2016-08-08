from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class SpelerForm(Form):
    naam = StringField('naam', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    categorie = StringField('categorie', validators=[DataRequired()])
