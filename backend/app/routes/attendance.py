from flask import Blueprint, request
from marshmallow import ValidationError

from app.schemas import AttendanceSchema
from app.services.attendance_service import AttendanceService

attendance_bp = Blueprint(
    "attendance",
    __name__,
    url_prefix="/api/attendances"
)

attendance_schema = AttendanceSchema()


@attendance_bp.route("", methods=["POST"])
def create_attendance():

    try:
        data = attendance_schema.load(request.get_json())

    except ValidationError as err:
        return {
            "errors": err.messages
        }, 400

    return AttendanceService.create(data)


@attendance_bp.route("", methods=["GET"])
def get_attendances():

    filters = {}

    employee_id = request.args.get("employee_id", type=int)
    attendance_date = request.args.get("attendance_date")
    status = request.args.get("status")

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    if employee_id is not None:
        filters["employee_id"] = employee_id

    if attendance_date:
        filters["attendance_date"] = attendance_date

    if status:
        filters["status"] = status

    return AttendanceService.get_all(
        filters=filters,
        page=page,
        per_page=per_page
    )


@attendance_bp.route("/<int:attendance_id>", methods=["GET"])
def get_attendance(attendance_id):

    return AttendanceService.get_by_id(attendance_id)


@attendance_bp.route("/employee/<int:employee_id>", methods=["GET"])
def get_employee_attendance(employee_id):

    return AttendanceService.get_by_employee(employee_id)


@attendance_bp.route("/<int:attendance_id>/check-in", methods=["POST"])
def check_in(attendance_id):

    return AttendanceService.check_in(attendance_id)


@attendance_bp.route("/<int:attendance_id>/check-out", methods=["POST"])
def check_out(attendance_id):

    return AttendanceService.check_out(attendance_id)