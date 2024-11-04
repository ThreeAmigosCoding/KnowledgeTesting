from .models import User, Test, Question, Answer, Result
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

    password = fields.String(load_only=True)


class QuestionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        load_instance = True
        include_relationships = True

    # test = fields.Nested('TestSchema', exclude=('questions',))
    answers = fields.Nested('AnswerSchema', many=True)


class AnswerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        load_instance = True
        include_relationships = False


class TestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Test
        load_instance = True
        include_relationships = True

    author = fields.Nested(UserSchema, only=('first_name', 'last_name',))
    # questions = fields.List(fields.Nested(QuestionSchema, exclude=('answers',)))


class ResultSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Result
        load_instance = True
        include_relationships = True

    test = fields.Nested(TestSchema, exclude=('results',))
    student = fields.Nested(UserSchema, exclude=('test_results',))
