import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Questions(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    question = sqlalchemy.Column(sqlalchemy.String, unique=True)
    correct_answer = sqlalchemy.Column(sqlalchemy.String, unique=True)
    wrong_answer1 = sqlalchemy.Column(sqlalchemy.String, unique=True)
    wrong_answer2 = sqlalchemy.Column(sqlalchemy.String, unique=True)
    explanation = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f"{self.question}"



