from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField(validators=[DataRequired('incorrect email'), ])
    password = PasswordField(validators=[DataRequired()])
    password_again = PasswordField( validators=[DataRequired('password mismatch')])
    name = StringField(validators=[DataRequired()])
    submit = SubmitField('Войти')