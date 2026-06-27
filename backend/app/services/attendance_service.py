from datetime import datetime

from app.extensions import db
from app.models import Attendance, Employee
from app.schemas import AttendanceSchema

attendance_schema = AttendanceSchema()
attendances_schema = AttendanceSchema(many=True)

PRESENT_HOURS = 8
HALF_DAY_HOURS = 4


class AttendanceService:

    @staticmethod
    def create(data):

        employee = db.session.get(Employee, data["employee_id"])

        if not employee:
            return {
                "message": "Employee not found."
            }, 404

        existing_attendance = (
            Attendance.query.filter_by(
                employee_id=data["employee_id"],
                attendance_date=data["attendance_date"]
            ).first()
        )

        if existing_attendance:
            return {
                "message": "Attendance already exists for this employee on this date."
            }, 409

        attendance = Attendance(
            employee_id=data["employee_id"],
            attendance_date=data["attendance_date"]
        )

        db.session.add(attendance)
        db.session.commit()

        return attendance_schema.dump(attendance), 201

    @staticmethod
    def check_in(attendance_id):

        attendance = db.session.get(Attendance, attendance_id)

        if not attendance:
            return {
                "message": "Attendance record not found."
            }, 404

        if attendance.check_in:
            return {
                "message": "Employee has already checked in."
            }, 409

        attendance.check_in = datetime.utcnow()

        db.session.commit()

        return attendance_schema.dump(attendance), 200

    @staticmethod
    def check_out(attendance_id):

        attendance = db.session.get(Attendance, attendance_id)

        if not attendance:
            return {
                "message": "Attendance record not found."
            }, 404

        if not attendance.check_in:
            return {
                "message": "Employee has not checked in yet."
            }, 400

        if attendance.check_out:
            return {
                "message": "Employee has already checked out."
            }, 409

        attendance.check_out = datetime.utcnow()

        duration = attendance.check_out - attendance.check_in
        working_hours = duration.total_seconds() / 3600

        attendance.working_hours = round(working_hours, 2)

        if attendance.working_hours >= PRESENT_HOURS:
            attendance.status = "Present"
        elif attendance.working_hours >= HALF_DAY_HOURS:
            attendance.status = "Half Day"
        else:
            attendance.status = "Absent"

        db.session.commit()

        return attendance_schema.dump(attendance), 200

    @staticmethod
    def get_all(filters=None, page=1, per_page=10):

        query = Attendance.query

        if filters:

            if filters.get("employee_id"):
                query = query.filter(
                    Attendance.employee_id == filters["employee_id"]
                )

            if filters.get("attendance_date"):
                query = query.filter(
                    Attendance.attendance_date == filters["attendance_date"]
                )

            if filters.get("status"):
                query = query.filter(
                    Attendance.status == filters["status"]
                )

        pagination = (
            query.order_by(
                Attendance.attendance_date.desc()
            ).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
        )

        return {
            "items": attendances_schema.dump(pagination.items),
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        }, 200

    @staticmethod
    def get_by_id(attendance_id):

        attendance = db.session.get(Attendance, attendance_id)

        if not attendance:
            return {
                "message": "Attendance record not found."
            }, 404

        return attendance_schema.dump(attendance), 200

    @staticmethod
    def get_by_employee(employee_id):

        employee = db.session.get(Employee, employee_id)

        if not employee:
            return {
                "message": "Employee not found."
            }, 404

        attendances = (
            Attendance.query.filter_by(
                employee_id=employee_id
            )
            .order_by(
                Attendance.attendance_date.desc()
            )
            .all()
        )

        return attendances_schema.dump(attendances), 200