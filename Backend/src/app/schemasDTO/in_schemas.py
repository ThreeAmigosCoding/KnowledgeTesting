from marshmallow import Schema, fields, post_load, ValidationError
from ..models import Graph, Node, Edge
from datetime import datetime


class NodeSchemaInput(Schema):
    title = fields.Str(required=True)

    class Meta:
        unknown = "exclude"


class EdgeSchemaInput(Schema):
    source = fields.Nested(NodeSchemaInput, required=True)
    target = fields.Nested(NodeSchemaInput, required=True)

    class Meta:
        unknown = "exclude"


class GraphSchemaInput(Schema):
    title = fields.Str(required=True)
    nodes = fields.List(fields.Nested(NodeSchemaInput), required=True)
    edges = fields.List(fields.Nested(EdgeSchemaInput), required=True)

    class Meta:
        unknown = "exclude"


class AnswerSchemaInput(Schema):
    text = fields.Str(required=True)
    is_correct = fields.Boolean(default=False)

    class Meta:
        unknown = "exclude"


class QuestionSchemaInput(Schema):
    text = fields.Str(required=True)
    is_multichoice = fields.Boolean(default=False)
    node_id = fields.Int(required=False, allow_none=True, missing=None)
    answers = fields.List(fields.Nested(AnswerSchemaInput), required=True)

    class Meta:
        unknown = "exclude"


class TestSchemaInput(Schema):
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)
    graph_id = fields.Int(required=True)
    questions = fields.List(fields.Nested(QuestionSchemaInput), required=True)

    class Meta:
        unknown = "exclude"


class TestSubmissionSchemaInput(Schema):
    test_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    answers = fields.List(fields.Int(), required=True)



class GeneratedGraphSchemaInput(Schema):
    test_id = fields.Int(required=True)
    start_date = fields.Float(required=True)
    end_date = fields.Float(required=True)

    class Meta:
        unknown = "exclude"