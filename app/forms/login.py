from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired('incorrect email')])
    password = PasswordField(validators=[DataRequired('incorrect password')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')