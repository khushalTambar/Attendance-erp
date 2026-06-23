from app.extensions import db
from app.models import Department


class DepartmentService:

    @staticmethod
    def create(data):

        existing_department = Department.query.filter_by(
            name=data["name"]
        ).first()

        if existing_department:
            return {
                "message": "Department already exists."
            }, 409

        department = Department(
            name=data["name"],
            description=data.get("description")
        )

        db.session.add(department)
        db.session.commit()

        return {
            "message": "Department created successfully."
        }, 201

    @staticmethod
    def get_all():

        departments = Department.query.all()

        return departments

    @staticmethod
    def get_by_id(department_id):

        department = Department.query.get(department_id)

        if not department:
            return None

        return department

    @staticmethod
    def update(department, data):

        department.name = data["name"]
        department.description = data.get("description")

        db.session.commit()

        return {
            "message": "Department updated successfully."
        }, 200

    @staticmethod
    def delete(department):

        db.session.delete(department)
        db.session.commit()

        return {
            "message": "Department deleted successfully."
        }, 200