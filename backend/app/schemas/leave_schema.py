from marshmallow import Schema, fields


class LeaveSchema(Schema):
    id = fields.Int(dump_only=True)

    employee_id = fields.Int(required=True)

    leave_type = fields.Str(required=True)

    start_date = fields.Date(required=True)

    end_date = fields.Date(required=True)

    total_days = fields.Int(dump_only=True)

    reason = fields.Str(required=True)

    status = fields.Str(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)