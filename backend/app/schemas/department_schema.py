from marshmallow import Schema, fields, validate


class DepartmentSchema(Schema):

    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    description = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=255)
    )

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)