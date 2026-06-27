from marshmallow import Schema, fields, validate


class EmployeeSchema(Schema):

    id = fields.Int(dump_only=True)

    employee_code = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=20)
    )

    first_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    last_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    email = fields.Email(required=True)

    phone = fields.Str(required=False)

    designation = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    department_id = fields.Int(required=True)

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)