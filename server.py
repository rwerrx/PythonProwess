from random import shuffle, choice, sample

import flask
from flask import Flask, render_template, redirect, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from helpers import db_session
from helpers.question import Questions
from helpers import users
from helpers.users import User
from forms.LoginForm import LoginForm
from forms.informatics_answers_form import InformaticsAnswerForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

current_answers_frames = {}
current_answers_soundtracks = {}


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html', title='Главная страница', bgc='#F2D9FD')


@app.route("/informatics", methods=['GET', 'POST'])
def informatics():
    form = InformaticsAnswerForm()
    current_answers = []
    with app.app_context():
        db_sess = db_session.create_session()
        print("------1------")
    necessary_questions = sample(db_sess.query(Questions).all(), k=5)
    questions = []
    correct_answers = []
    form_answers = [form.answer1, form.answer2, form.answer3, form.answer4, form.answer5]

    for i in range(5):
        correct_answers.append(necessary_questions[i].correct_answer)
        list_of_answers = [necessary_questions[i].correct_answer, necessary_questions[i].wrong_answer1,
                           necessary_questions[i].wrong_answer2]
        questions.append(necessary_questions[i].question)
        shuffle(list_of_answers)
        form_answers[i].choices = list_of_answers
    current_answers[current_user.id] = correct_answers
    if form.validate_on_submit():
        all_result = []
        cnt_cor_answers = 0
        for i, answer in enumerate(list(form)[:-2]):
            result = [correct_answers[i], necessary_questions[i], answer.data]
            all_result.append(result)
            if current_answers[current_user.id][i] == answer.data:
                cnt_cor_answers += 1

        return render_template('points.html', title='ответы', result=all_result, cnt=cnt_cor_answers)
    return render_template('informatics.html', questions=questions, correct_answers=correct_answers,
                           form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/play')
def play():
    return render_template('play.html')


@app.route('/location')
def location():
    return 'локация'


@app.route('/rules')
def rules():
    return render_template('rules.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация', form=form, bgc="#E0CEFB")


@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def not_allowed(error):
    return render_template('405.html'), 405


def main():
    db_session.global_init("./db/base.sqlite")
    db_sess = db_session.create_session()
    user = db_sess.query(User).first()
    app.run(debug=True, port="8080")


if __name__ == '__main__':
    main()
