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
