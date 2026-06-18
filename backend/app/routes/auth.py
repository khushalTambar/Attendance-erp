from flask import Blueprint, request
from marshmallow import ValidationError

from app.schemas.auth_schema import RegisterSchema
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

register_schema = RegisterSchema()


@auth_bp.route("/register", methods=["POST"])
def register():

    try:
        data = register_schema.load(request.get_json())

    except ValidationError as err:
        return {
            "errors": err.messages
        }, 400

    return AuthService.register(data)