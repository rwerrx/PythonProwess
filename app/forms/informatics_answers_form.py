from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired


class InformaticsAnswerForm(FlaskForm):
    answer1 = RadioField(choices=[], default=1, validators=[DataRequired('choose an answer')], validate_choice=False)
    answer2 = RadioField(choices=[], default=1, validators=[DataRequired('choose an answer')], validate_choice=False)
    answer3 = RadioField(choices=[], default=1, validators=[DataRequired('choose an answer')], validate_choice=False)
    answer4 = RadioField(choices=[], default=1, validators=[DataRequired('choose an answer')], validate_choice=False)
    answer5 = RadioField(choices=[], default=1, validators=[DataRequired('choose an answer')], validate_choice=False)
    answer6 = RadioField(choices=[], default=1, validators=[DataRequired('choose an answer')], validate_choice=False)
    answer7 = RadioField(choices=[], default=1, validators=[DataRequired('choose an answer')], validate_choice=False)


    

    submit = SubmitField('Ответить')
