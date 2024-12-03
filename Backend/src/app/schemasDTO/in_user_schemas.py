from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    class Meta:
        unknown = "exclude"

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    role = fields.Str(validate=validate.OneOf(["student", "teacher"]), required=True)

    class Meta:
        unknown = "exclude"