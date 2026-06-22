from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token


class AuthService:

    @staticmethod
    def register(data):

        if User.query.filter_by(email=data["email"]).first():
            return {
                "message": "Email already exists."
            }, 409

        if User.query.filter_by(employee_id=data["employee_id"]).first():
            return {
                "message": "Employee ID already exists."
            }, 409

        user = User(
            employee_id=data["employee_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            role=data.get("role", "employee")
        )

        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return {
            "message": "User registered successfully."
        }, 201
        
    @staticmethod
    def login(data):

        user = User.query.filter_by(email=data["email"]).first()

        if not user:
            return {
                "message": "Invalid email or password."
            }, 401

        if not user.check_password(data["password"]):
            return {
                "message": "Invalid email or password."
            }, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "email": user.email,
                "role": user.role
            }
        )

        return {
            "message": "Login successful.",
            "access_token": access_token
        }, 200