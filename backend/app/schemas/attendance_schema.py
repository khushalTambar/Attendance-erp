from marshmallow import Schema, fields


class AttendanceSchema(Schema):
    id = fields.Int(dump_only=True)

    employee_id = fields.Int(required=True)

    attendance_date = fields.Date(required=True)

    check_in = fields.DateTime(dump_only=True)

    check_out = fields.DateTime(dump_only=True)

    working_hours = fields.Float(dump_only=True)

    status = fields.Str(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)