from app.extensions import db
from app.models import Leave, Employee
from app.schemas import LeaveSchema

leave_schema = LeaveSchema()
leaves_schema = LeaveSchema(many=True)


class LeaveService:

    @staticmethod
    def create(data):

        employee = db.session.get(Employee, data["employee_id"])

        if not employee:
            return {
                "message": "Employee not found."
            }, 404

        if data["end_date"] < data["start_date"]:
            return {
                "message": "End date cannot be before start date."
            }, 400

        total_days = (
            data["end_date"] - data["start_date"]
        ).days + 1

        leave = Leave(
            employee_id=data["employee_id"],
            leave_type=data["leave_type"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            total_days=total_days,
            reason=data["reason"]
        )

        db.session.add(leave)
        db.session.commit()

        return leave_schema.dump(leave), 201

    @staticmethod
    def get_all():

        leaves = Leave.query.order_by(
            Leave.created_at.desc()
        ).all()

        return leaves_schema.dump(leaves), 200

    @staticmethod
    def get_by_id(leave_id):

        leave = db.session.get(Leave, leave_id)

        if not leave:
            return {
                "message": "Leave request not found."
            }, 404

        return leave_schema.dump(leave), 200

    @staticmethod
    def approve(leave_id):

        leave = db.session.get(Leave, leave_id)

        if not leave:
            return {
                "message": "Leave request not found."
            }, 404

        leave.status = "Approved"

        db.session.commit()

        return leave_schema.dump(leave), 200

    @staticmethod
    def reject(leave_id):

        leave = db.session.get(Leave, leave_id)

        if not leave:
            return {
                "message": "Leave request not found."
            }, 404

        leave.status = "Rejected"

        db.session.commit()

        return leave_schema.dump(leave), 200