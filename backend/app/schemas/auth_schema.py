from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    employee_id = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    email = fields.Email(required=True)

    password = fields.Str(
        required=True,
        validate=validate.Length(min=8)
    )

    role = fields.Str(load_default="employee")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)