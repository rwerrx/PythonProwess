from random import sample

from helpers import db_session
from helpers.question import Questions
from forms.informatics_answers_form import InformaticsAnswerForm
from server import app
form = InformaticsAnswerForm()
with app.app_context():

    db_sess = db_session.create_session()

necessary_questions = sample(db_sess.query(Questions).all(), k=3)
correct_answers = []
form_answers = [form.answer1, form.answer2, form.answer3]

for i in range(3):
    correct_answers.append(necessary_questions[i].correct_answer)
    form_answers[i].choices = necessary_questions[i][2:]

print(form_answers, necessary_questions, correct_answers)