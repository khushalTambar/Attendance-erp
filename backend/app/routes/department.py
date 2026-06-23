from flask import Blueprint, request
from marshmallow import ValidationError

from app.models import Department
from app.schemas.department_schema import DepartmentSchema
from app.services.department_service import DepartmentService

department_bp = Blueprint(
    "department",
    __name__,
    url_prefix="/api/departments"
)

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


@department_bp.route("", methods=["POST"])
def create_department():

    try:
        data = department_schema.load(request.get_json())

    except ValidationError as err:
        return {
            "errors": err.messages
        }, 400

    return DepartmentService.create(data)


@department_bp.route("", methods=["GET"])
def get_departments():

    departments = DepartmentService.get_all()

    return departments_schema.dump(departments), 200


@department_bp.route("/<int:department_id>", methods=["GET"])
def get_department(department_id):

    department = DepartmentService.get_by_id(department_id)

    if not department:
        return {
            "message": "Department not found."
        }, 404

    return department_schema.dump(department), 200


@department_bp.route("/<int:department_id>", methods=["PUT"])
def update_department(department_id):

    department = DepartmentService.get_by_id(department_id)

    if not department:
        return {
            "message": "Department not found."
        }, 404

    try:
        data = department_schema.load(request.get_json())

    except ValidationError as err:
        return {
            "errors": err.messages
        }, 400

    return DepartmentService.update(department, data)


@department_bp.route("/<int:department_id>", methods=["DELETE"])
def delete_department(department_id):

    department = DepartmentService.get_by_id(department_id)

    if not department:
        return {
            "message": "Department not found."
        }, 404

    return DepartmentService.delete(department)