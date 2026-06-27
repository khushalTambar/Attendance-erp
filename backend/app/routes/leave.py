from flask import Blueprint, request
from marshmallow import ValidationError

from app.schemas import LeaveSchema
from app.services.leave_service import LeaveService

leave_bp = Blueprint(
    "leave",
    __name__,
    url_prefix="/api/leaves"
)

leave_schema = LeaveSchema()


@leave_bp.route("", methods=["POST"])
def create_leave():

    try:
        data = leave_schema.load(request.get_json())

    except ValidationError as err:
        return {
            "errors": err.messages
        }, 400

    return LeaveService.create(data)


@leave_bp.route("", methods=["GET"])
def get_leaves():

    return LeaveService.get_all()


@leave_bp.route("/<int:leave_id>", methods=["GET"])
def get_leave(leave_id):

    return LeaveService.get_by_id(leave_id)


@leave_bp.route("/<int:leave_id>/approve", methods=["PUT"])
def approve_leave(leave_id):

    return LeaveService.approve(leave_id)


@leave_bp.route("/<int:leave_id>/reject", methods=["PUT"])
def reject_leave(leave_id):

    return LeaveService.reject(leave_id)