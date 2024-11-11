from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from ..database import db
from ..models import Test, Question, Answer
from ..schemas import TestSchema, QuestionSchema
from ..schemasDTO.in_schemas import TestSchemaInput


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


def create_test(request_body):
    test_schema = TestSchemaInput()
    try:
        test_data = test_schema.load(request_body)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    test = Test(
        title=test_data['title'],
        author_id=test_data['author_id'],
        graph_id=test_data['graph_id']
    )
    db.session.add(test)
    db.session.flush()

    for question_data in test_data['questions']:
        question = Question(
            text=question_data['text'],
            is_multichoice=question_data['is_multichoice'],
            node_id=question_data['node_id'],
            test_id=test.id
        )
        db.session.add(question)
        db.session.flush()

        for answer_data in question_data['answers']:
            answer = Answer(
                text=answer_data['text'],
                is_correct=answer_data['is_correct'],
                question_id=question.id
            )
            db.session.add(answer)

    try:
        db.session.commit()
        return jsonify(test_schema.dump(test)), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500