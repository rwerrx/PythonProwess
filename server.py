from flask import Flask, render_template, redirect, jsonify, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from random import sample, shuffle
from helpers import db_session
from helpers.question import Questions
from helpers import users
from helpers.users import User
from forms.login import LoginForm
from forms.informatics_answers_form import InformaticsAnswerForm
from forms.user import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


all_tests = {}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница', bgc='#F2D9FD')


@app.route("/informatics", methods=['GET', 'POST'])
@login_required
def informatics():
    form = InformaticsAnswerForm()
    db_sess = db_session.create_session()
    if request.method == "GET":
        
        necessary_questions = sample(db_sess.query(Questions).all(), k=5)
        all_tests[current_user.id] = necessary_questions
        questions = []
        correct_answers = []
        explanation = []
        form_answers = [form.answer1, form.answer2, form.answer3, form.answer4, form.answer5]

        for i in range(5):
            correct_answers.append(necessary_questions[i].correct_answer)
            list_of_answers = [necessary_questions[i].correct_answer, necessary_questions[i].wrong_answer1,
                               necessary_questions[i].wrong_answer2]
            questions.append(necessary_questions[i].question)
            explanation.append(necessary_questions[i].explanation)
            shuffle(list_of_answers)
            form_answers[i].choices = list_of_answers
        return render_template('informatics.html', questions=questions, correct_answers=correct_answers,
                               form=form, exp=explanation)

    if form.validate_on_submit():
        answers = [request.form.get("answer1"), request.form.get("answer2"), request.form.get("answer3"),
                     request.form.get("answer4"), request.form.get("answer5")]
        all_result = []
        cnt_cor_answers = 0
        for i, answer in enumerate(list(form)[:-2]):


            print(db_sess.query(Questions).filter(Questions.question == all_tests[current_user.id][i].question))

            
            all_result.append([all_tests[current_user.id][i].question, all_tests[current_user.id][i].correct_answer,
                               all_tests[current_user.id][i].explanation, answers[i]])
            if all_tests[current_user.id][i].correct_answer == answers[i]:
                cnt_cor_answers += 1


        return render_template('points.html', title='ответы', result=all_result, cnt=cnt_cor_answers, bgc='#E0CEFB')


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
    return render_template('login.html', title='Авторизация', form=form,  bgc='#E0CEFB')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")



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
                           title='Регистрация', form=form,  bgc='#E0CEFB')




def main():
    db_session.global_init("db/base.sqlite")
    db_sess = db_session.create_session()
    user = db_sess.query(User).first()
    app.run(debug=True, port="8100")


if __name__ == '__main__':
    main()
