from marshmallow import Schema, fields, post_load
from ..models import Graph, Node, Edge

class NodeSchema(Schema):
    title = fields.Str(required=True)
    class Meta:
        unknown = "exclude"

class EdgeSchema(Schema):
    source = fields.Nested(NodeSchema, required=True)
    target = fields.Nested(NodeSchema, required=True)
    class Meta:
        unknown = "exclude"

class GraphSchema(Schema):
    title = fields.Str(required=True)
    nodes = fields.List(fields.Nested(NodeSchema), required=True)
    edges = fields.List(fields.Nested(EdgeSchema), required=True)
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
    node_id = fields.Int(required=True)
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