from .models import User, Test, Question, Answer, Result, Node, Edge, Graph
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
    questions = fields.List(fields.Nested(QuestionSchema))


class ResultSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Result
        load_instance = True
        include_relationships = True

    test = fields.Nested(TestSchema)
    student = fields.Nested(UserSchema, only=('first_name', 'last_name',))
    student_answers = fields.Method("get_student_answers")

    def get_student_answers(self, obj):
        answers_by_question = {}
        for student_answer in obj.student_answers:
            question_id = student_answer.answer.question.id
            if question_id not in answers_by_question:
                answers_by_question[question_id] = []
            answers_by_question[question_id].append(student_answer.answer.id)

        return {
            question_id: answer_ids
            for question_id, answer_ids in answers_by_question.items()
        }


class NodeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Node
        load_instance = True
        include_relationships = False


class EdgeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Edge
        load_instance = True
        include_relationships = True

    source = fields.Str(attribute="source.title")
    target = fields.Str(attribute="target.title")


class GraphSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Graph
        load_instance = True
        include_relationships = True

    nodes = fields.Nested('NodeSchema', many=True)
    edges = fields.Nested('EdgeSchema', many=True)
