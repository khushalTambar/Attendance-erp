from flask import Blueprint, request
from marshmallow import ValidationError

from app.schemas.employee_schema import EmployeeSchema
from app.services.employee_service import EmployeeService

employee_bp = Blueprint(
    "employee",
    __name__,
    url_prefix="/api/employees"
)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


@employee_bp.route("", methods=["POST"])
def create_employee():

    try:
        data = employee_schema.load(request.get_json())

    except ValidationError as err:
        return {
            "errors": err.messages
        }, 400

    return EmployeeService.create(data)


@employee_bp.route("", methods=["GET"])
def get_employees():

    return EmployeeService.get_all()


@employee_bp.route("/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):

    return EmployeeService.get_by_id(employee_id)