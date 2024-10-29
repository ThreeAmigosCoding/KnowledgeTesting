from flask import jsonify

from ..database import db
from ..models import Test, Question
from ..schemas import TestSchema, QuestionSchema


def get_tests(author_id):
    tests = Test.query.filter(Test.author_id == author_id).all()
    test_schema = TestSchema(many=True)
    return jsonify(test_schema.dump(tests))


def get_test_questions(test_id):
    questions = Question.query.filter(Question.test_id == test_id).all()
    question_schema = QuestionSchema(many=True)
    return jsonify(question_schema.dump(questions))


def get_test_by_id(test_id):
    tests = Test.query.filter(Test.id == test_id).first()
    test_schema = TestSchema(many=False)
    return jsonify(test_schema.dump(tests))