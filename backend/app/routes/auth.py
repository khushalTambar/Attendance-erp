from flask import Blueprint, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User
from app.schemas.auth_schema import RegisterSchema
from app.services.auth_service import AuthService
from app.schemas.auth_schema import RegisterSchema, LoginSchema

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
login_schema = LoginSchema()

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
@auth_bp.route("/login", methods=["POST"])
def login():

    try:
        data = login_schema.load(request.get_json())

    except ValidationError as err:
        return {
            "errors": err.messages
        }, 400

    return AuthService.login(data)

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return {
            "message": "User not found."
        }, 404

    return {
        "id": user.id,
        "employee_id": user.employee_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role
    }, 200